import find_solution as fs
import requests
import json
import os
import re
import sys
import platform
import time

def path_based_on_os(path):
    return path.replace("/", "\\") if platform.system() == 'Windows' else path.replace("\\", "/")

sys.path.append(path_based_on_os(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")))

from aws_helper import upload_dict_to_s3, send_to_sqs, poll_from_sqs, download_from_s3
from constants import HTML_VALIDATOR_SQS, JS_SYNTAX_CHECKER_BUCKET, JS_SYNTAX_CHECKER_DATA_FILENAME, PARENT_SQS_RESULT, PARENT_BUCKET, CHILD_BUCKET, HTML_VALIDATOR_BUCKET, HTML_VALIDATOR_DATA_FILENAME, HTML_VALIDATOR_SQS_RESULT


def validate_html_list(url_list):
    output = {}
    counter=0
    for url in url_list:
        #in order to show demo in presentation
        if counter == 10:
            return output
        print("~~checking next url~~\n")
        output[url] = validate_html(url)
        counter+=1
    return output


def validate_html(url):
    """
    Sends a GET request to the W3C Markup Validation Service with the specified URL and returns the validation results as JSON.
    """
    # Construct the URL for the validation request
    api_url = "https://validator.w3.org/nu/?doc={}&out=json".format(url)

    # Send a GET request to the API and get the response
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()



def fix_output_values(output):
    print("prepearing data and searching for solution\n")
    wanted_info_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'resources','w3_wanted_info.json') 
    with open(wanted_info_path, 'r') as f:
        needed_info = json.load(f)
    new_output = {}
    # counter=0
    for i in output.values():
        if i is not None:
            for k, v in i.items():
                if k == 'url':
                    # counter+=1
                    # prec =  counter / list_len
                    # print("checking next url (" + prec + "%)\n")
                    url = v
                    new_output[url] = []
                if k == 'messages':
                    messages = v
                    for msg in messages:
                        tmp_dic = {}
                        tmp_dic["lastLine"] = -1
                        tmp_dic["lastColumn"] = -1 
                        tmp_dic["firstColumn"] = -1
                        for title, info in msg.items():
                            if title in needed_info:
                                if title == 'type':
                                    if info == 'info':
                                        tmp_dic["priority"] = "low"
                                    elif info == 'error':
                                        tmp_dic["priority"] = "medium"
                                    else:
                                        tmp_dic["priority"] = "medium"
                                if title == 'message':
                                    info = re.sub(r'\u201c(.+?)\u201d', '', info)
                                tmp_dic[title] = info
                        tmp_dic["block_code"] = []
                        tmp_dic["type"] = "HTML standard issue"
                        tmp_dic["suggestions"] = fs.get_solution(tmp_dic['message'])
                        new_output[url].append(tmp_dic)
    return new_output


def write_output_to_json(output):
    # Return the validation results as JSON
    with open(os.path.join('resources','validation_results.json'), 'w') as f:
        json.dump(output, f, indent=4)


is_cloud = 'CLOUD' in os.environ
while True:
    if is_cloud:
        bucket_path = poll_from_sqs(HTML_VALIDATOR_SQS)
        raw_data = download_from_s3(PARENT_BUCKET, bucket_path)
        
    else:
        raw_data = sys.argv[1]
        # start_url = "http://testphp.vulnweb.com"
        # start_url = "https://www.realpython.com"

    print("~~Starting html_validator worker~~\n")
    urls_list = raw_data["all_urls"]
    # global list_len
    # list_len=len(url_list)
    output = validate_html_list(urls_list)
    output = fix_output_values(output)

    index = bucket_path.find(".com")
    if index != -1:
        bucket_path = bucket_path[:index + 4]  # Include the ".com" substring

    result_file_path = bucket_path + "/" + HTML_VALIDATOR_DATA_FILENAME
    upload_dict_to_s3(HTML_VALIDATOR_BUCKET,result_file_path,output)

    print(f'Uploading bucket path to {HTML_VALIDATOR_SQS_RESULT} SQS')
    send_to_sqs(HTML_VALIDATOR_SQS_RESULT, result_file_path)
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n")
    # write_output_to_json(output)

