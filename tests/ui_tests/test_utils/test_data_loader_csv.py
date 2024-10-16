import csv
from modules.constants import Data


def resolve_data_constant(value):
    """
    Replaces strings like 'Data.USER_EMAIL' with actual values from the Data class.
    If the value does not reference Data, returns the original value.
    """
    if value.startswith('Data.'):
        attribute_name = value.split('.')[1]
        return getattr(Data, attribute_name, value)
    return value


def get_test_data_by_test_name(filename, test_name):
    """
    Loads test data from a CSV file and dynamically builds a list of dictionaries
    excluding the 'test_name' field. Replaces string references to constants in the Data class.
    Returns a list of dictionaries, where each dictionary contains data for a single test case.
    """
    test_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['test_name'] == test_name:
                resolved_row = {key: resolve_data_constant(value) for key, value in row.items() if key != 'test_name'}
                test_data.append(resolved_row)
    return test_data


def get_test_data(filename, test_name):
    """
    Loads test data from a CSV file and dynamically builds a list of tuples
    excluding the 'test_name' field. Replaces string references to constants in the Data class.
    Returns a list of tuples, where each tuple contains data for a single test case.
    """
    test_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['test_name'] == test_name:
                resolved_row = tuple(resolve_data_constant(value) for key, value in row.items() if key != 'test_name')
                test_data.append(resolved_row)
    return test_data
