import os
import csv
from misc.badminton_data_cleaner.process_doubles_file import ProcessDoublesFile


class BatchProcessDoublesFiles:

    @staticmethod
    def process_files(data_source_dir_path, doubles_type, destination_file_path):
        consolidated_data = {
            'dates': [],
        }
        relevant_file_paths = BatchProcessDoublesFiles.get_relevant_file_paths(data_source_dir_path, doubles_type)
        for file_path in relevant_file_paths:
            data = ProcessDoublesFile.process_file(file_path)
            for key in data:
                # keys are either the player names or 'date'
                if key is 'date':
                    consolidated_data['dates'].append(data[key])
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
                        'data': [new_data],
                    }
        print(consolidated_data)
        BatchProcessDoublesFiles.write_file(destination_file_path, consolidated_data)

    @staticmethod
    def write_file(destination_file_path, consolidated_data):
        # # processed_headers = False
        # for data in consolidated_data:

        with open(destination_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Country', 'Image']
            fieldnames.extend(consolidated_data['dates'])
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for key in consolidated_data:
                if key is 'dates':
                    continue

                row = {
                    'Name': key,
                    'Country': consolidated_data[key]['country']
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
                if doubles_type == 'md':
                    look_for = "Men's doubles"
                elif doubles_type == 'wd':
                    look_for = "Women's doubles"
                else:
                    look_for = "Mixed doubles"

                # print('look_for: ' + look_for)
                for filename in os.listdir(dir_path + directory):
                    # print('filename: ' + filename)
                    if not filename.startswith('.') and look_for in filename:
                        file_paths.append(dir_path + directory + '/' + filename)
            except NotADirectoryError:
                # print('not a directory')
                continue
        # print(file_paths)
        return file_paths


