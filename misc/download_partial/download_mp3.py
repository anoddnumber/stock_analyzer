import subprocess
import csv


with open('video_feed.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if len(row) < 1:
            print('Row does not have enough arguments, at least 3 expected: {}'.format(row))
            continue

        url = row[0]

        try:
            print('Trying to download video with url: {}'.format(url))
            bashCommand = './download_mp3.bash {}'.format(url)
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        except Exception as error:
            print('ERROR: Could not download video with url: {}'.format(url))
            print(error)

print("DOWNLOAD COMPLETE")