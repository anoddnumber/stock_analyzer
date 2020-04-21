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

                    name = p1_last_name.upper() + '/' + p2_last_name.upper()

                    # hacks for mixed doubles
                    if name == 'MATEUSIAK/ZIEBA *':
                        name = 'MATEUSIAK/ZIEBA'
                    if date == '2012-04-05':
                        ret['ZHANG/ZHAO'] = {
                            'points': '90940'
                        }
                        ret['XU/MA'] = {
                            'points': '84196.2'
                        }
                        ret['AHMAD/NATSIR'] = {
                            'points': '80990'
                        }
                        ret['FISCHER NIELSEN/PEDERSEN'] = {
                            'points': '80036.39999999999',
                        }
                        ret['CHEN/CHENG'] = {
                            'points': '66822.39999999999'
                        }
                        ret['LAYBOURN/RYTTER JUHL'] = {
                            'points': '64782.8571'
                        }
                        ret['LEE/HA'] = {
                            'points': '57470'
                        }
                        ret['CHAN/GOH'] = {
                            'points': '56460'
                        }
                        ret['PRAPAKAMOL/THOUNGTHONGKAM'] = {
                            'points': '54874'
                        }
                        ret['ADCOCK/BANKIER'] = {
                            'points': '49880',
                            'country': 'ENG',
                            'image': 'https://badmintonbites.com/wp-content/uploads/2020/01/england_flag.png'
                        }

                    #hacks for womens doubles
                    # if date == '2012-04-05':
                    #     ret['WANG/YU'] = {
                    #         'points': '100704.9444'
                    #     }
                    #     ret['TIAN/ZHAO'] = {
                    #         'points': '91051.9161'
                    #     }
                    #     ret['HA/KIM'] = {
                    #         'points': '76540'
                    #     }
                    #     ret['FUJII/KAKIWAA'] = {
                    #         'points': '70214.61199999999',
                    #         'country': 'JPN',
                    #         'image': Constants.flag_map['JPN'],
                    #     }
                    #     ret['MAEDA/SUETSUNA'] = {
                    #         'points': '63604.6607'
                    #     }
                    #     ret['MATSUO/NAITO'] = {
                    #         'points': '62283.9'
                    #     }
                    #     ret['RYTTER JUHL/PEDERSEN'] = {
                    #         'points': '61599.8937'
                    #     }
                    #     ret['POLII/JAUHARI'] = {
                    #         'points': '55247.862'
                    #     }
                    #     ret['CHENG/CHIEN'] = {
                    #         'points': '54949.7'
                    #     }
                    #     ret['JUNG/KIM'] = {
                    #         'points': '54680'
                    #     }


                    # hacks for mens doubles
                    # if name == 'CHUNG/LEE':
                    #     name = 'JUNG/LEE'
                    # if name == 'HOON/TAN ~':
                    #     name = 'HOON/TAN'
                    # if date == '2012-04-05':
                    #     ret['CAI/FU'] = {
                    #         'points': '96011.3057',
                    #     }
                    #     ret['JUNG/LEE'] = {
                    #         'points': '89561.30039999999',
                    #     }
                    #     ret['BOE/MOGENSEN'] = {
                    #         'points': '76157.2683',
                    #     }
                    #     ret['KO/YOO'] = {
                    #         'points': '76047.30740000001',
                    #     }
                    #     ret['CHAI/GUO'] = {
                    #         'points': '67549.8184',
                    #     }
                    #     ret['AHSAN/SEPTANO'] = {
                    #         'points': '63329.3044',
                    #     }
                    #     ret['HASHIMOTO/HIRATA'] = {
                    #         'points': '61958.1569',
                    #     }
                    #     ret['KOO/TAN'] = {
                    #         'points': '59491.3903',
                    #     }
                    #     ret['KAWAMAE/SATO'] = {
                    #         'points': '57847.2',
                    #     }
                    #     ret['FANG/LEE'] = {
                    #         'points': '57839.3004',
                    #     }
                    #     return ret

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


# ProcessDoublesFile.process_file('/Volumes/ExFAT_B/Samson/badmintonbites/bwf_historical_data/csv/WR 2012-01-05 (Week 1)/Men\'s doubles-Table 1.csv')