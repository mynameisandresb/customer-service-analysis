import csv
from datetime import datetime

def time_conversion(timestr):
    for timeformat in ["%m/%d/%Y %I:%M:%S %p", "%m-%d-%y %H:%M"]:
        try:
            return datetime.strptime(timestr, timeformat)
        except ValueError:
            pass
    raise ValueError('Incompatible time format for conversion')

def main():
    csv_dict = {}
    with open('Dataset/311_Service_Requests_from_2010_to_Present.csv', 'r') as file:
        csv_reader = csv.reader(file)
        column_names = next(csv_reader)
        csv_data = []
        for row in csv_reader:
            csv_dict = {}
            for key, value in zip(column_names, row):
                if value and (key == 'Created Date' or key == 'Closed Date'):
                    value = time_conversion(value)
                csv_dict[key] = value
            csv_data.append(csv_dict)
main()