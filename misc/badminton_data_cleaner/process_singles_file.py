import csv
from misc.badminton_data_cleaner.constants import Constants


class ProcessSinglesFile:

    @staticmethod
    def process_file(file_path):
        date = file_path.split(sep=' ')[1]
        ret = {'date': date}

        # print('file_path: ' + file_path)
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # print(row)
                try:
                    # data is in a different format for 2012-04-05
                    if date == '2012-04-05':
                        rank = int(row[6])
                        last_name = row[1]
                        first_name = row[2]
                        country = row[5]
                        points = row[7]
                    else:
                        rank = int(row[0])
                        last_name = row[2]
                        first_name = row[3]
                        country = row[5]
                        points = row[6]

                    if country == 'MAS' or country == 'CHN' or country == 'KOR' or country == 'THA' or country == "TPE" or country == 'HKG':
                        name = last_name.upper() + ' ' + first_name.upper()
                    else:
                        name = first_name.upper() + ' ' + last_name.upper()

                    ret[name] = {
                        'country': country,
                        'points': points,
                        'image': Constants.flag_map[country],
                    }

                    if rank >= 10:
                        break
                except ValueError:
                    continue
        # print(ret)
        return ret


# ProcessDoublesFile.process_file('/Volumes/ExFAT_B/Samson/badmintonbites/bwf_historical_data/csv/WR 2012-01-05 (Week 1)/Men\'s doubles-Table 1.csv')