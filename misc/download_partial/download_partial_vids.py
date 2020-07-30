import subprocess
import csv


with open('video_feed.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if len(row) < 3:
            print('Row does not have enough arguments, at least 3 expected: {}'.format(row))
            continue

        url = row[0]
        start_time = row[1]
        end_time = row[2]

        try:
            print('Trying to download video with url: {}, start time: {}, and end time: {}'.format(url, start_time, end_time))
            bashCommand = './download_partial.bash {} {} {}'.format(url, start_time, end_time)
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        except Exception:
            print('ERROR: Could not download video with url: {url}, start time: {}, and end time: {}'
                  .format(start_time, end_time))

    try:
        print('Executing convert_to_mov.bash')
        bashCommand = './convert_to_mov.bash'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    except Exception:
        print('ERROR: There was a problem executing convert_to_mov.bash')

print("DOWNLOAD COMPLETE")