import traceback
import sys
import csv


class TRACEBACK:
    def __init__(self):
        print("tracking Errors started")

    def tracebackError(self, function_name='', date=''):
        Errors = traceback.format_exc().split('During')[0].split('\n')
        file = Errors[1].split(',')
        filename = file[0]
        lineno = file[1]
        line_containing_error = Errors[2]
        error_type = Errors[3]
        Error_list = [filename, lineno, line_containing_error, error_type, function_name, date]
        with open('traceback_log.csv', 'a', newline='', encoding='cp437') as openFile:
            writer = csv.writer(openFile)
            writer.writerow(Error_list)
            print(Error_list)
