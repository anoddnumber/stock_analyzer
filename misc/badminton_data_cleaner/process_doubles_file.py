import csv


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
                    ret[name] = {
                        'country': p1_country,
                        'points': points,
                        # 'rank': rank,
                    }

                    if rank >= 10:
                        break
                except ValueError:
                    continue
        # print(ret)
        return ret


