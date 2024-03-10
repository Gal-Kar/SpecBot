import json
import re
import os
from googlesearch import search

def keep_only_console_logs(url_content_dict):
    new_dict = {}
    pattern = re.compile(r'"console_logs": [(.*?)]', re.DOTALL)
    for url,content in url_content_dict.items():
        new_dict[url] = pattern.findall(content)
    return new_dict

def create_url_content_dict(raw_data_file):
    file=read_json_file(raw_data_file)
    url_content_dict = {}
    for url in file:
        for title in file[url]:
            if title == "content":
                url_content_dict[url]=file[url][title]

    return keep_only_scripts(url_content_dict)

def search_google(query):
    search_results = []
    try:
        for j in search(query, tld="co.in", num=3, stop=3, pause=0):
            search_results.append(j)
    except:
        search_results.append("No solution due to google search api limits")
    
    return search_results

def get_solution(msg):
    query = "rocket validator " + msg
    return search_google(query)