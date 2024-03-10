import raw_data_helper as rd
import js_checker_helper as check_function
import os
import json
import sys
import platform

def path_based_on_os(path):
    return path.replace("/", "\\") if platform.system() == 'Windows' else path.replace("\\", "/")

sys.path.append(path_based_on_os(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")))

from aws_helper import upload_dict_to_s3, send_to_sqs, poll_from_sqs, download_from_s3
from constants import JS_SYNTAX_CHECKER_SQS, JS_SYNTAX_CHECKER_BUCKET, JS_SYNTAX_CHECKER_DATA_FILENAME, PARENT_SQS_RESULT, PARENT_BUCKET, CHILD_BUCKET, JS_SYNTAX_CHECKER_SQS_RESULT

is_cloud = 'CLOUD' in os.environ

while True:
    if is_cloud:
        bucket_path = poll_from_sqs(JS_SYNTAX_CHECKER_SQS)
        raw_data = download_from_s3(PARENT_BUCKET, bucket_path)
        
    else:
        raw_data = sys.argv[1]
        # start_url = "http://testphp.vulnweb.com"
        # start_url = "https://www.realpython.com"


    # raw_data = argv[0]
    # raw_data = os.path.join('resources','raw-data.json')
    reduced_data = rd.create_url_content_dict(raw_data)

    #search keywords dictionary
    replace_keywords_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'resources','replace_keywords.json') 
    with open(replace_keywords_path, 'r') as f:
        replace_keywords = json.load(f)

    #result dictionary

    result = {}
    print("~~Starting js_checker worker~~\n")
    # go over each url
    # counter = 1
    size = len(reduced_data)
    for url in reduced_data:
        # prec = counter/reduced_data
        # print("-- "+ prec +"% --")
        # counter+=1
        tmp_dict ={}
        result[url] = []
        tmp_dict["priority"] = "low"
        tmp_dict["type"] = "Syntax Error"
        tmp_dict["lastLine"] = -1
        tmp_dict["lastColumn"] = -1
        tmp_dict["firstColumn"] = -1
        tmp_dict["message"] = ""
        tmp_dict["suggestions"] = []
        #go over each content block:
        for block in reduced_data[url]:
            tmp_dict["block_code"] = []
            counter = 0
            for word in block.split(' '):
                if word in replace_keywords:
                    function_to_call = getattr(check_function, replace_keywords[word])
                    output = function_to_call(block,counter)
                    if(output):
                        tmp_dict["block_code"].append(output)
                counter += 1
            if len(tmp_dict["block_code"]) != 0:
                result[url].append(tmp_dict)
            else:
                del result[url]

    index = bucket_path.find(".com")
    if index != -1:
        bucket_path = bucket_path[:index + 4]  # Include the ".com" substring

    result_file_path = bucket_path + "/" + JS_SYNTAX_CHECKER_DATA_FILENAME
    upload_dict_to_s3(JS_SYNTAX_CHECKER_BUCKET,result_file_path,result)
    print(f'Uploading bucket path to {JS_SYNTAX_CHECKER_SQS_RESULT} SQS')
    send_to_sqs(JS_SYNTAX_CHECKER_SQS_RESULT, result_file_path)
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n")
    # rd.write_dict_to_file(result,"js_checker_result.json")
