"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- views.py --

@author: Informed Solutions
"""
import datetime
import uuid
import json
import logging
import requests
import traceback

import xmltodict as xmltodict
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import CardPaymentRequestSerializer, PaypalPaymentRequestSerializer, ApiKeySerializer
from .utilities import Utilities
from lxml import etree

# initiate logging
log = logging.getLogger('django.server')

# Initiate worldpay endpoint URL
WORLDPAY_PAYMENT_ENDPOINT = settings.WORLDPAY_PAYMENT_ENDPOINT

# Initiate endpoint credentials
MERCHANT_CODE = settings.MERCHANT_CODE
WORLDPAY_XML_USERNAME = settings.WORLDPAY_XML_USERNAME
WORLDPAY_XML_PASSWORD = settings.WORLDPAY_XML_PASSWORD


@api_view(['PUT'])
def change_api_key(request):
    """
    Function for updating the Worldpay API key used by the payment gateway API
    :param request: a json request object detailing the new API key to be used
    :return: a success or failure indicator as to whether the Worldpay API key has been updated
    """
    # Change API Key, this is the exact same as the Notify version
    try:
        mapped_json_request = Utilities.convert_json_to_python_object(request.data)
        serializer = ApiKeySerializer(data=mapped_json_request)
        if serializer.is_valid():
            # API key set
            global MERCHANT_CODE
            MERCHANT_CODE = mapped_json_request['api_key']
            return JsonResponse({"message": "Api key successfully updated"}, status=200)
        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request", }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


@api_view(['GET'])
def get_payment(request, payment_id):
    """
    Function for retrieving a previously placed order
    :param request: a json request issued over http protocols, this must exist (like a class' self method)
    :param payment_id: the order code of the previously issued payment
    :return: a json representation of a previously lodged payment
    """
    payload = __build_get_payment_request(payment_id)
    headers = {"content-type": "text/xml"}
    response = requests.post(WORLDPAY_PAYMENT_ENDPOINT, data=payload, headers=headers,
                             auth=(WORLDPAY_XML_USERNAME, WORLDPAY_XML_PASSWORD))

    dictionary = xmltodict.parse(response.text)
    payment_service_result = dictionary.get('paymentService')
    payment_service_result_reply = payment_service_result.get('reply')

    if 'error' in payment_service_result_reply.get('orderStatus'):
        if payment_service_result_reply.get('orderStatus').get('error').get('@code') == '5':
            return JsonResponse(
                {
                    "message": 'Payment not found',
                    "error": payment_service_result_reply.get('orderStatus').get('error').get('#text')
                }, status=404
            )
        else:
            return JsonResponse(
                {
                    "message": 'Internal Server error',
                    "error": payment_service_result_reply.get('orderStatus').get('error').get('#text')
                }, status=500
            )

    # If no errors were encountered in retrieving the payment compile payment date
    payment_date_day = int(payment_service_result_reply.get('orderStatus').get('date').get('@dayOfMonth'))
    payment_date_month = int(payment_service_result_reply.get('orderStatus').get('date').get('@month'))
    payment_date_year = int(payment_service_result_reply.get('orderStatus').get('date').get('@year'))
    payment_date_hour = int(payment_service_result_reply.get('orderStatus').get('date').get('@hour'))
    payment_date_minute = int(payment_service_result_reply.get('orderStatus').get('date').get('@minute'))
    payment_date_second = int(payment_service_result_reply.get('orderStatus').get('date').get('@second'))

    payment_date_combined = datetime.datetime(payment_date_year, payment_date_month, payment_date_day,
                                              payment_date_hour, payment_date_minute, payment_date_second)

    return JsonResponse(
        {
            "orderCode": payment_id,
            "paymentMethod": payment_service_result_reply.get('orderStatus').get('payment').get('paymentMethod'),
            "creationDate": payment_date_combined.isoformat(),
            "lastEvent": payment_service_result_reply.get('orderStatus').get('payment').get('lastEvent'),
            "amount": payment_service_result_reply.get('orderStatus').get('payment').get('amount').get('@value'),
            "currencyCode": payment_service_result_reply.get('orderStatus').get('payment').get('amount').get(
                '@currencyCode')
        }, status=200
    )


def __build_get_payment_request(payment_id):
    """
    Helper method for creating a request object that can be consumed by the Worldpay XML API to get the latest status of an order.
    :param payment_id the order code for a payment
    """
    payment_service_root = etree.Element('paymentService', version='1.4', merchantCode=str(MERCHANT_CODE))
    inquiry = etree.SubElement(payment_service_root, 'inquiry')
    etree.SubElement(inquiry, 'orderInquiry', orderCode=str(payment_id))

    # Append DTD heading to request
    xml_string = etree.tostring(
        payment_service_root.getroottree(),
        xml_declaration=True,
        encoding='UTF-8',
        doctype='<!DOCTYPE paymentService PUBLIC "-//Worldpay//DTD Worldpay PaymentService v1//EN" "http://dtd.worldpay.com/paymentService_v1.dtd">'
    )

    return xml_string


@api_view(['POST'])
def make_card_payment(request):
    """
    Function for making a new card payment via the WorldPay payment processing platform
    :param request: a json object inclusive of details for a card payment to be taken
    :return: a success or failure response from the WorldPay payment processing platform
    """
    mapped_json_request = Utilities.convert_json_to_python_object(request.data)

    try:

        serializer = CardPaymentRequestSerializer(data=mapped_json_request)

        if serializer.is_valid():

            # If dev environment mock the answer from worldpay
            if hasattr(settings, 'DEV_MODE'):
                if settings.DEV_MODE:
                    return JsonResponse({"orderCode": str(uuid.uuid4())}, status=201)

            return __create_worldpay_card_order_request(mapped_json_request)

        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])

        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


def __create_worldpay_card_order_request(card_payment_request):
    """
    Helper method for creating a request object that can be consumed by the Worldpay API to take a card payment
    :param card_payment_request: a request object sent to the payment gateway API containing information for taking a
    card payment via Worldpay
    """
    payload = __build_worldpay_card_payment_xml(card_payment_request)
    headers = {"content-type": "text/xml"}
    response = requests.post(WORLDPAY_PAYMENT_ENDPOINT, data=payload, headers=headers,
                             auth=(WORLDPAY_XML_USERNAME, WORLDPAY_XML_PASSWORD))
    dictionary = xmltodict.parse(response.text)

    payment_service_result = dictionary.get('paymentService')
    payment_service_result_reply = payment_service_result.get('reply')

    if 'error' in payment_service_result_reply:
        return JsonResponse(
            {
                "message": 'Internal Server error',
                "error": payment_service_result_reply.get('error').get('#text')
            }, status=500
        )
    else:
        return JsonResponse(
            {
                "customerOrderCode": payment_service_result_reply.get('orderStatus').get('@orderCode')
            }
            , status=201)


def __build_worldpay_card_payment_xml(card_payment_request):
    """
    Helper method for creating an XML request object for dispatch to the Worldpay API
    :param card_payment_request: an inbound payment request received by the payment gateway API
    :return: a structured XML request to be POSTed to Worldpay
    """
    payment_service_root = etree.Element('paymentService', version='1.4', merchantCode=str(MERCHANT_CODE))
    submit = etree.SubElement(payment_service_root, 'submit')
    order = etree.SubElement(submit, 'order', orderCode=str(card_payment_request['customer_order_code']))

    description = etree.SubElement(order, 'description')
    description.text = card_payment_request['order_description']

    etree.SubElement(
        order, 'amount', currencyCode=str(card_payment_request['currency_code']),
        exponent='2', value=str(card_payment_request['amount'])
    )

    payment_details_element = etree.SubElement(order, 'paymentDetails')
    card_ssl = etree.SubElement(payment_details_element, 'CARD-SSL')

    card_number = etree.SubElement(card_ssl, 'cardNumber')
    card_number.text = str(card_payment_request['card_number'])

    expiry_date = etree.SubElement(card_ssl, 'expiryDate')
    etree.SubElement(
        expiry_date, 'date',
        month=str(card_payment_request['expiry_month']),
        year=str(card_payment_request['expiry_year'])
    )

    card_holder = etree.SubElement(card_ssl, 'cardHolderName')
    card_holder.text = str(card_payment_request['card_holder_name'])

    # Append DTD heading to request
    xml_string = etree.tostring(
        payment_service_root.getroottree(),
        xml_declaration=True,
        encoding='UTF-8',
        doctype='<!DOCTYPE paymentService PUBLIC "-//Worldpay//DTD Worldpay PaymentService v1//EN" "http://dtd.worldpay.com/paymentService_v1.dtd">'
    )

    return xml_string


@api_view(['POST'])
def make_paypal_payment(request):
    """
    Function for making a new Paypal payment via the WorldPay payment processing platform
    :param request: a json object inclusive of details for a paypal payment to be taken
    :return: a response inclusive of any URLs that a user should be redirected to (i.e. WorldPay paypal UIs) for making
    a Paypal payment
    """
    mapped_json_request = Utilities.convert_json_to_python_object(request.data)

    try:
        serializer = PaypalPaymentRequestSerializer(data=mapped_json_request)
        if serializer.is_valid():
            return __create_worldpay_paypal_order_request(mapped_json_request)
        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


def __create_worldpay_paypal_order_request(paypal_payment_request):
    """
    Helper method for creating a request object that can be consumed by the Worldpay XML API to take a paypal payment
    :param paypal_payment_request: a request object sent to the payment gateway API containing information for taking a
    Paypal payment via Worldpay
    """
    payload = __build_worldpay_paypal_payment_xml(paypal_payment_request)
    headers = {"content-type": "text/xml"}
    response = requests.post(WORLDPAY_PAYMENT_ENDPOINT, data=payload, headers=headers,
                             auth=(WORLDPAY_XML_USERNAME, WORLDPAY_XML_PASSWORD))
    dictionary = xmltodict.parse(response.text)

    payment_service_result = dictionary.get('paymentService')
    payment_service_result_reply = payment_service_result.get('reply')

    if 'error' in payment_service_result_reply.get('orderStatus'):
        return JsonResponse(
            {
                "message": 'Internal Server error',
                "error": payment_service_result_reply.get('orderStatus').get('error').get('#text')
            }, status=500
        )
    else:
        return JsonResponse(
            {
                "amount": payment_service_result_reply.get('orderStatus').get('payment').get('amount').get('@value'),
                "customerOrderCode": payment_service_result_reply.get('orderStatus').get('@orderCode'),
                "paymentMethod": payment_service_result_reply.get('orderStatus').get('payment').get('paymentMethod'),
                "currencyCode": payment_service_result_reply.get('orderStatus').get('payment').get('amount').get(
                    '@currencyCode'),
                "redirectUrl": payment_service_result_reply.get('orderStatus').get('payment').get('redirectUrl'),
            }
            , status=201)


def __build_worldpay_paypal_payment_xml(paypal_payment_request):
    """
    Helper method for creating an XML request object for dispatch to the Worldpay API
    :param paypal_payment_request: an inbound paypal payment request received by the payment gateway API
    :return: a structured XML request to be POSTed to Worldpay
    """
    payment_service_root = etree.Element('paymentService', version='1.2', merchantCode=str(MERCHANT_CODE))
    submit = etree.SubElement(payment_service_root, 'submit')
    order = etree.SubElement(
        submit, 'order', orderCode=str(paypal_payment_request['customer_order_code']),
        shopperLanguageCode=str(paypal_payment_request['shopperCountryCode'])
    )

    description = etree.SubElement(order, 'description')
    description.text = paypal_payment_request['order_description']

    etree.SubElement(
        order, 'amount', currencyCode=str(paypal_payment_request['currency_code']),
        exponent='2', value=str(paypal_payment_request['amount'])
    )

    payment_details_element = etree.SubElement(order, 'paymentDetails')
    paypal_express = etree.SubElement(payment_details_element, 'PAYPAL-EXPRESS')

    success_url = etree.SubElement(paypal_express, 'successURL')
    success_url.text = str(paypal_payment_request['success_url'])

    failure_url = etree.SubElement(paypal_express, 'failureURL')
    failure_url.text = str(paypal_payment_request['failure_url'])

    cancel_url = etree.SubElement(paypal_express, 'cancelURL')
    cancel_url.text = str(paypal_payment_request['cancellation_url'])

    # Append DTD heading to request
    xml_string = etree.tostring(
        payment_service_root.getroottree(),
        xml_declaration=True,
        encoding='UTF-8',
        doctype='<!DOCTYPE paymentService PUBLIC "-//Bibit//DTD Bibit PaymentService v1//EN" "http://dtd.bibit.com/paymentService_v1.dtd">'
    )

    return xml_string


def __format_error(ex):
    """
    Helper function for formatting errors encountered when serializing Django requests
    :param ex: the exception encountered by a Django serializer
    :return: a json friendly response detailing an exception incurred whilst serializing a request
    """
    # Formatting default Django error messages
    err = str(ex).split(":", 1)
    err[0] = err[0].strip('{')
    err[1] = err[1].strip('}')
    err[1] = err[1].replace('[', '')
    err[1] = err[1].replace(']', '')
    return err
