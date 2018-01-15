"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- utilities.py --

@author: Informed Solutions
"""

import re


class Utilities:
    """
    A helper class for utility functions
    """

    @staticmethod
    def convert_json_to_python_object(json_object):
        """
        Helper method for converting a json (camelCase) object to
        a python object using properties that adhere to a PEP8 underscore
        delimited convention
        :param json_object: the json object to be converted to a python object
        :return: a python object representing the converted json object
        """
        out = {}
        for json_key in json_object:
            python_key = Utilities.__convert(json_key)
            if isinstance(json_object[json_key], dict):
                out[python_key] = Utilities.convertJSON(json_object[json_key])
            elif isinstance(json_object[json_key], list):
                out[python_key] = Utilities.__convert_json_array(json_object[json_key])
            else:
                out[python_key] = json_object[json_key]
        return out

    def __convert_json_array(a):
        """
        Private helper method for converting a json array to a python array
        :return: a python array representation of the request object
        """
        python_array = []
        for i in a:
            if isinstance(i, list):
                python_array.append(Utilities.__convert_json_array(i))
            elif isinstance(i, dict):
                python_array.append(Utilities.__convert_json_array(i))
            else:
                python_array.append(i)
        return python_array

    def __convert(key):
        """
        A helper method for converting an object key from camelCase to
        python underscore delimited syntax
        :return: a python key name based on the supplied camelCase name
        """
        a = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
        return a.sub(r'_\1', key).lower()
