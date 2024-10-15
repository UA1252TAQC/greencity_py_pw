import csv

def get_test_data_by_test_name(filename, test_name):
    test_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['test_name'] == test_name:
                test_data.append((row['language'], row['email'], row['password'], row['expected']))
    return test_data
