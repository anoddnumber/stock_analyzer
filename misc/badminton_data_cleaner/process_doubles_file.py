import csv
from misc.badminton_data_cleaner.constants import Constants


class ProcessDoublesFile:

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
                    rank = int(row[0])
                    p1_last_name = row[2]
                    p1_country = row[5]
                    p2_last_name = row[7]
                    points = row[11]

                    name = p1_last_name + '/' + p2_last_name

                    # hacks for mens doubles
                    if name == 'CHUNG/LEE':
                        name = 'JUNG/LEE'
                    if name == 'HOON/TAN ~':
                        name = 'HOON/TAN'
                    if date == '2012-04-05':
                        ret['CAI/FU'] = {
                            'points': '96011.3057',
                        }
                        ret['JUNG/LEE'] = {
                            'points': '89561.30039999999',
                        }
                        ret['BOE/MOGENSEN'] = {
                            'points': '76157.2683',
                        }
                        ret['KO/YOO'] = {
                            'points': '76047.30740000001',
                        }
                        ret['CHAI/GUO'] = {
                            'points': '67549.8184',
                        }
                        ret['AHSAN/SEPTANO'] = {
                            'points': '63329.3044',
                        }
                        ret['HASHIMOTO/HIRATA'] = {
                            'points': '61958.1569',
                        }
                        ret['KOO/TAN'] = {
                            'points': '59491.3903',
                        }
                        ret['KAWAMAE/SATO'] = {
                            'points': '57847.2',
                        }
                        ret['FANG/LEE'] = {
                            'points': '57839.3004',
                        }
                        return ret

                    ret[name] = {
                        'country': p1_country,
                        'points': points,
                        'image': Constants.flag_map[p1_country],
                        # 'rank': rank,
                    }

                    if rank >= 10:
                        break
                except ValueError:
                    continue
        # print(ret)
        return ret


ProcessDoublesFile.process_file('/Volumes/ExFAT_B/Samson/badmintonbites/bwf_historical_data/csv/WR 2012-01-05 (Week 1)/Men\'s doubles-Table 1.csv')