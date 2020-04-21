import os
import csv
from misc.badminton_data_cleaner.process_singles_file import ProcessSinglesFile


class BatchProcessSinglesFiles:

    @staticmethod
    def process_files(data_source_dir_path, singles_type, destination_file_path):
        consolidated_data = {
            'dates': [],
        }
        relevant_file_paths = BatchProcessSinglesFiles.get_relevant_file_paths(data_source_dir_path, singles_type)
        for file_path in relevant_file_paths:
            data = ProcessSinglesFile.process_file(file_path)

            consolidated_data['dates'].append(data['date'])
            for key in data:
                # keys are either the player names or 'date'
                if key is 'date':
                    continue

                new_data = {
                    'date': data['date'],
                    'points': data[key]['points'],
                }

                if key in consolidated_data:
                    consolidated_data[key]['data'].append(new_data)
                else:
                    consolidated_data[key] = {
                        'country': data[key]['country'],
                        'image': data[key]['image'],
                        'data': [new_data],
                    }

                BatchProcessSinglesFiles.write_file(destination_file_path, consolidated_data)

    @staticmethod
    def write_file(destination_file_path, consolidated_data):
        dates = consolidated_data['dates']
        dates.sort()

        with open(destination_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Country', 'Image']
            fieldnames.extend(dates)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval=0)

            writer.writeheader()

            for key in consolidated_data:
                if key is 'dates':
                    continue

                row = {
                    'Name': key,
                    'Country': consolidated_data[key]['country'],
                    'Image': consolidated_data[key]['image'],
                }

                for datum in consolidated_data[key]['data']:
                    row[datum['date']] = datum['points']
                writer.writerow(row)

    @staticmethod
    def get_relevant_file_paths(dir_path, doubles_type):
        file_paths = []
        for directory in os.listdir(dir_path):
            try:
                # print('directory ' + directory)
                if doubles_type == 'ms':
                    look_for = "men's singles"
                else:
                    look_for = "women's singles"

                for filename in os.listdir(dir_path + directory):
                    if not filename.startswith('.') and filename.lower().startswith(look_for):
                        file_paths.append(dir_path + directory + '/' + filename)
            except NotADirectoryError:
                continue
        return file_paths


BatchProcessSinglesFiles.process_files('/Volumes/ExFAT_B/Samson/badmintonbites/bwf_historical_data/csv/', 'ms',
                                       '/Volumes/ExFAT_B/Samson/badmintonbites/test.csv')