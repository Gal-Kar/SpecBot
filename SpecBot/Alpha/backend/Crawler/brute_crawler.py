import sys
import os
from urllib.parse import urlparse
import requests
import signal

from helpers import path_based_on_os, write_to_json, signal_handler

sys.path.append(path_based_on_os(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")))

from aws_helper import upload_dict_to_s3, send_to_sqs, poll_from_sqs
from constants import BRUTE_SQS, BRUTE_SQS_RESULT, BRUTE_BUCKET, BRUTE_DATA_FILENAME

is_cloud = 'CLOUD' in os.environ
signal.signal(signal.SIGINT, signal_handler)

vulnerable_paths = [
    '/admin',
    '/dashboard',
    '/login',
    '/register',
    '/api',
    '/dev',
    '/config',
    '/feed',
    '/comments/feed'
    '/wp-admin',
    '/wp-content',
    '/wp-content/plugins',
    '/wp-content/themes',
    '/wp-includes',
    '/wp-login',
    '/wp-login.php'
    '/wp-admin/admin-ajax',
    '/wp-json',
    '/xmlrpc.php',
    '/wp-links-opml.php',
    '/wp-mail.php',
    '/wp-trackback.php',
    '/readme.html',
    '/license.txt',
    '/wp-register.php',
    '/wp-activate.php',
    '/wp-signup.php',
    '/wp-blog-header.php',
    '/wp-comments-post.php',
    '/wp-config.php',
    '/wp-sitemap.xml',
    '/wp-cron.php',
    '/wp-config.php',
    '/wp-admin/setup-config.php',
    '/phpmyadmin',
    '/config.php',
    '/phpinfo.php',
    '/backup.sql',
    '/backup',
    '/uploads',
    '/includes',
    '/vendor',
    '/cgi-bin',
    '/error_log',
    '/server-status',
    '/rails/info/properties',
    '/rails/info/routes',
    '/rails/info/seed',
    '/rails/console',
    '/rails/db',
    '/rails/dbconsole',
    '/rails/log',
    '/users/sign_in',
    '/.htaccess',
    '/icons',
    '/_api/wix-smush-server/',
    '/sitemap.xml',
    '/robots.txt',
    '/humans.txt',
    '/_api/wix-public-html-renderer/',
    '/ngsw.json',
    '/ngsw/state',
    '/compiler.js',
    '/logs',
    '/system',
    '/tmp',
    '/upload',
    '/backup_files',
    '/debugger',
    '/zone.js',
    '/actuator',
    '/h2-console',
    '/management',
    '/env',
    '/trace',
    '/metrics',
    '/beans',
    '/manager',
    '/web-inf',
    '/struts',
    '/struts2',
    '/struts3',
    '/action',
    '/struts-config',
    '/struts.properties',
    '/test',
    '/bin',
    '/App_Data',
    '/App_Code',
    '/Config',
    '/Logs',
    '/Scripts',
    '/settings',
    '/administrator',
    '/pgAdmin',
    '/pgadmin4',
    '/pg_hba.conf',
    '/pg_ident.conf',
    '/psql',
    '/_admin',
    '/_debug',
    '/_debug/trigger_agent',
    '/_setup',
    '/_status',
    '/_system',
    '/api/alerts',
    '/api/datasources',
    '/api/plugins',
    '/api/admin/settings',
    '/api/auth/keys',
    '/jquery.js',
    '/jquery.min.js',
    '/js/jquery.js',
    '/js/jquery.min.js',
    '/assets/js/jquery.js',
    '/assets/js/jquery.min.js',
    '/lib/jquery.js',
    '/lib/jquery.min.js',
    '/public/js/jquery.js',
    '/public/js/jquery.min.js',
    '/services',
    '/h4x0r' # backdoor
    ]

class BruteCrawler:
    def __init__(self, start_url):
        self.start_url = start_url
        parsed_url = urlparse(self.start_url)
        self.base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
        self.pages_data = {}

    def send_data(self):
        if is_cloud:
            bucket_path = f'{self.start_url}/{BRUTE_DATA_FILENAME}'
            print(f'Uploading brute data to {BRUTE_BUCKET} S3')
            upload_dict_to_s3(BRUTE_BUCKET, bucket_path, self.pages_data)
            print('Done')

            print(f'Posting brute bucket path to {BRUTE_SQS_RESULT} SQS')
            send_to_sqs(BRUTE_SQS_RESULT, bucket_path)
            print('Done')
        else:
            write_to_json(BRUTE_DATA_FILENAME, self.pages_data)

    def begin_scrapping(self):
        for path in vulnerable_paths:
            url = self.base_url + path
            response = requests.get(url)
            if response.status_code == 200:
                print('**********************************************************')
                print(f'Found vulnerability: {url}')
                print('**********************************************************')
                self.pages_data[url] = {
                    'headers': dict(response.headers),
                    'status_code': 200,
                    'content': response.text,
                    'suspect': 'true'
                }
        return self


while True:
    if is_cloud:
        start_url = poll_from_sqs(BRUTE_SQS)
    else:
        start_url = sys.argv[1]
        # start_url = "http://testphp.vulnweb.com"
        # start_url = "https://www.realpython.com"
    BruteCrawler(start_url).begin_scrapping().send_data()