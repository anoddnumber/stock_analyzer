import subprocess
import csv


# bashCommand = "./download_partial.bash https://www.youtube.com/watch?v=MY24WxxlMuA 00:10:20 00:22:10"
# process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()

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
            print(f'Could not download video with url: {url}, start time: {start_time}, and end time: {end_time}')

print("DOWNLOAD COMPLETE")