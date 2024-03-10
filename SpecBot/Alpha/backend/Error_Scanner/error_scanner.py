import os
import json
import sys
import platform
import error_scanner_helper as eh

def path_based_on_os(path):
    return path.replace("/", "\\") if platform.system() == 'Windows' else path.replace("\\", "/")

sys.path.append(path_based_on_os(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")))

from aws_helper import upload_dict_to_s3, send_to_sqs, poll_from_sqs, download_from_s3
from constants import ERROR_SCANNER_SQS, ERROR_SCANNER_BUCKET, ERROR_SCANNER_DATA_FILENAME, PARENT_SQS_RESULT, PARENT_BUCKET, CHILD_BUCKET, ERROR_SCANNER_SQS_RESULT

is_cloud = 'CLOUD' in os.environ

while True:
    if is_cloud:
        bucket_path = poll_from_sqs(ERROR_SCANNER_SQS)
        raw_data = download_from_s3(PARENT_BUCKET, bucket_path)
        
    else:
        raw_data = sys.argv[1]


    print("~~Starting console error worker~~\n")
    console_log = {}
    for url in raw_data:
        console_log[url] = []
        for title in raw_data[url]:
            if title == "console_logs":
                for log in raw_data[url][title]:
                    cur_log = {}
                    if log["level"] == "WARNING":
                        cur_log["priority"] = "medium"
                    elif log["level"] == "SEVERE" or log["level"] == "Critical" or log["level"] == "Fatal":
                        cur_log["priority"] = "high"
                    else:
                        continue
                    cur_log["type"] = "Console Error"
                    cur_log["lastLine"] = -1
                    cur_log["lastColumn"] = -1
                    cur_log["firstColumn"] = -1
                    cur_log["message"] = log["message"]
                    cur_log["block_code"] = []
                    cur_log["suggestions"] = eh.get_solution(log['message'])
                    console_log[url].append(cur_log)
                if len(console_log[url]) == 0:
                    del console_log[url]

    del console_log['all_urls']
    index = bucket_path.find(".com")
    if index != -1:
        bucket_path = bucket_path[:index + 4]  # Include the ".com" substring

    result_file_path = bucket_path + "/" + ERROR_SCANNER_DATA_FILENAME
    upload_dict_to_s3(ERROR_SCANNER_BUCKET,result_file_path,console_log)
    print(f'Uploading bucket path to {ERROR_SCANNER_SQS_RESULT} SQS')
    send_to_sqs(ERROR_SCANNER_SQS_RESULT, result_file_path)
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n")
    # rd.write_dict_to_file(result,"js_checker_result.json")