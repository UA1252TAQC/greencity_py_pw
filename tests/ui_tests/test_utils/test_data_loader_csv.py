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
    Loads test data from a CSV file and replaces string references to constants in the Data class.
    Returns a list of lists, each containing data for a single test case.
    """
    test_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['test_name'] == test_name:
                language = resolve_data_constant(row['language'])
                email = resolve_data_constant(row['email'])
                password = resolve_data_constant(row['password'])
                expected = resolve_data_constant(row['expected'])
                test_data.append([language, email, password, expected])
    return test_data
