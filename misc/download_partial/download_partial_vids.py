import subprocess
import csv


with open('video_feed.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if len(row) != 3:
            continue

        url = row[0]
        start_time = row[1]
        end_time = row[2]

        try:
            print(f'Trying to download video with url: {url}, start time: {start_time}, and end time: {end_time}')
            bashCommand = f'./download_partial.bash {url} {start_time} {end_time}'
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        except Exception:
            print(f'ERROR: Could not download video with url: {url}, start time: {start_time}, and end time: {end_time}')

    try:
        print('Executing convert_to_mov.bash')
        bashCommand = './convert_to_mov.bash'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    except Exception:
        print('ERROR: There was a problem executing convert_to_mov.bash')

print("DOWNLOAD COMPLETE")