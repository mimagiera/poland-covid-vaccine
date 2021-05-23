import os
import time

conversation_ids = []

conversation_ids_file = open("not_download_yet_ids.txt", "r")
for line in conversation_ids_file:
    conversation_ids.append(line.split("\"")[1])
conversation_ids_file.close()


_total_count = len(conversation_ids)
_current_count = 0
_current_progress = 0
_begin_time = time.time()

since_date = "2021-05-01"
data_dir = "data_from_scrap/threads"

try:
    os.makedirs(data_dir)
except FileExistsError:
    # directory already exists
    pass

for conversation_id in conversation_ids:
    print(f"Getting tweets from thread: {conversation_id} since date: {since_date}")

    data_file = f"{data_dir}/{conversation_id}.json"
    os.system(
        f'snscrape --jsonl --progress --since {since_date} twitter-search "conversation_id:{conversation_id} lang:pl"> {data_file}')

    _current_count += 1
    _current_progress = (100*_current_count)/_total_count
    print("Progress: {}".format(_current_progress) + "  Estimated time: {}".format((time.time()-_begin_time)*(100-_current_progress)/_current_progress/3600))
