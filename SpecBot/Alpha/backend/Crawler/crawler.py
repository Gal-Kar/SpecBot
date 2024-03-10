import subprocess
import concurrent.futures
import os
import sys
import signal

from helpers import write_to_json, path_based_on_os, read_json_file, signal_handler

sys.path.append(path_based_on_os(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")))

from aws_helper import upload_dict_to_s3, download_from_s3, send_to_sqs, poll_from_sqs
from constants import CHILD_SQS, CHILD_SQS_RESULT, CHILD_BUCKET, CHILD_DATA_FILENAME, \
                      PARENT_SQS, PARENT_BUCKET, PARENT_DATA_FILENAME, \
                      BRUTE_SQS, BRUTE_SQS_RESULT, BRUTE_BUCKET, BRUTE_DATA_FILENAME, \
                      VULNERABILITY_SCANNER_SQS, JS_SYNTAX_CHECKER_SQS, HTML_VALIDATOR_SQS, ERROR_SCANNER_SQS

is_cloud = 'CLOUD' in os.environ
signal.signal(signal.SIGINT, signal_handler)

# if is_cloud:
#     start_url = poll_from_sqs(PARENT_SQS)
#     result_file_path = f'{start_url}/{PARENT_DATA_FILENAME}'
# else:
#     start_url = sys.argv[1]
    # start_url = "http://testphp.vulnweb.com"
    # start_url = "https://www.realpython.com"

def start_crawlers():
    if is_cloud:
        start_cloud_crawlers()
    else:
        start_local_crawlers()

##################################### LOCAL #####################################

def start_local_crawlers():
    start_url = sys.argv[1]

    crawler_folder_path = path_based_on_os(os.path.dirname(os.path.abspath(__file__)))
    workers_path = child_crawlers_paths(crawler_folder_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers = len(workers_path)) as executor:
        futures = []
        for worker_path in workers_path:
            futures.append(executor.submit(subprocess.Popen, ['python', worker_path, start_url]))

    # wait for all of them to finish
    for future in concurrent.futures.as_completed(futures):
        future.result().wait()

    collect_local_data_to_single_file()

def child_crawlers_paths(crawler_folder_path):
    args = []
    for crawler_name in ['brute_crawler', 'child_crawler']:
        child_crawler_path = path_based_on_os(f'{crawler_folder_path}/{crawler_name}.py')
        args.append(child_crawler_path)

    return args

def collect_local_data_to_single_file():
    child_data = read_json_file(CHILD_DATA_FILENAME)
    brute_data = read_json_file(BRUTE_DATA_FILENAME)

    brute_data.update(child_data)

    write_to_json(PARENT_DATA_FILENAME, brute_data)

##################################### LOCAL #####################################

##################################### CLOUD #####################################

def start_cloud_crawlers():
    start_url = poll_from_sqs(PARENT_SQS)
    result_file_path = f'{start_url}/{PARENT_DATA_FILENAME}'

    print(f'Starting crawlers to go over {start_url}')
    send_to_sqs(CHILD_SQS, start_url)
    send_to_sqs(BRUTE_SQS, start_url)
    collect_cloud_data_to_single_bucket(result_file_path)

def collect_cloud_data_to_single_bucket(result_file_path):
    print('Waiting for brute crawler result')
    brute_bucket_path = poll_from_sqs(BRUTE_SQS_RESULT)
    brute_data = download_from_s3(BRUTE_BUCKET, brute_bucket_path)
    print('Got brute data')

    print('Waiting for brute crawler result')
    child_bucket_path = poll_from_sqs(CHILD_SQS_RESULT)
    child_data = download_from_s3(CHILD_BUCKET, child_bucket_path)
    print('Got child data')

    brute_data.update(child_data)

    upload_dict_to_s3(PARENT_BUCKET, result_file_path, brute_data)

    print(f'Uploading bucket path to {VULNERABILITY_SCANNER_SQS} SQS')
    send_to_sqs(VULNERABILITY_SCANNER_SQS, result_file_path)
    print('Done')

    print(f'Uploading bucket path to {JS_SYNTAX_CHECKER_SQS} SQS')
    send_to_sqs(JS_SYNTAX_CHECKER_SQS, result_file_path)
    print('Done')

    print(f'Uploading bucket path to {HTML_VALIDATOR_SQS} SQS')
    send_to_sqs(HTML_VALIDATOR_SQS, result_file_path)
    print('Done')

    print(f'Uploading bucket path to {ERROR_SCANNER_SQS} SQS')
    send_to_sqs(ERROR_SCANNER_SQS, result_file_path)
    print('Done')

##################################### CLOUD #####################################

while True:
    start_crawlers()
