import csv
from concurrent import futures
from ffmpy import FFmpeg
from subprocess import check_call
from pdb import set_trace
import subprocess
import os
import io
import sys

num_threads = 4
output_folder = 'downloads'

videos = []
with open('videos_to_annotate.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")

    for row in reader:
        videos.append({
            'id': row['youtube_id'],
            'start': row['time_start'],
            'end': row['time_end']
        })

# Download and cut a clip to size
def dl_and_cut(vid):
    print("Downloading {}".format(vid))
    # Use youtube_dl to download the video
    FNULL = open(os.devnull, 'w')
    check_call(['youtube-dl', \
        #'--no-progress', \
        '-f','best[ext=mp4]', \
        '-o',output_folder +'/'+vid['id']+'_temp.mp4', \
        'youtu.be/'+vid['id'] ], \
        stdout=FNULL,stderr=subprocess.STDOUT
        )

    # Verify that the video has been downloaded. Skip otherwise
    if os.path.exists(output_folder+'/'+vid['id']+'_temp.mp4'):
        # Cut out the clip within the downloaded video and save the clip
        # in the correct class directory. Full re-encoding is used to maintain
        # frame accuracy. See here for more detail:
        # http://www.markbuckler.com/post/cutting-ffmpeg/
        check_call(['ffmpeg',\
        '-i','file:'+output_folder+'/'+vid['id']+'_temp.mp4',\
        '-ss', str(float(vid['start'])),\
        '-strict','-2',\
        '-t', str((float(vid['end'])-float(vid['start']))),\
        '-threads','1',\
        output_folder+'/'+vid['id']+'.mp4'],
            stdout=FNULL,stderr=subprocess.STDOUT )

    # Remove the temporary video
    os.remove(output_folder+'/'+vid['id']+'_temp.mp4')

if __name__ == '__main__':
    with futures.ProcessPoolExecutor(max_workers=num_threads) as executor:
        fs = [executor.submit(dl_and_cut,vid) for vid in videos]
        for i, f in enumerate(futures.as_completed(fs)):
            # Write progress to error so that it can be seen
            sys.stderr.write( \
                "Downloaded video: {} / {} \r".format(i, len(videos)))