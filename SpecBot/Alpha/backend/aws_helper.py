import boto3
import json
import os

encode_type = 'utf-8'

def get_bucket_worker_bucket_path(file_path, worker_name):
    filename = os.path.basename(file_path)
    return f'{worker_name}/{filename}'

def get_region_and_account_id():
    region = os.environ['AWS_DEFAULT_REGION']
    account_id = os.environ['AWS_ACCOUNT_ID']
    return [region, account_id]

def poll_from_sqs(queue_name):
    # use environment variable for account_id & region (?)
    print(f'\n\nStarting polling from {queue_name} SQS')

    sqs_client = boto3.client('sqs')
    region, account_id = get_region_and_account_id()
    queue_url = f'https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}'
    count = 0
    # create a limit for max amount of polling (?)

    while True:
        count += 1
        print(f'Starting {count} polling from {queue_name}')
        response = sqs_client.receive_message(
            QueueUrl = queue_url,
            MaxNumberOfMessages = 1,
            WaitTimeSeconds = 20
        )
        if 'Messages' not in response: continue

        message = response['Messages'][0] # receive only 1 message
        body = message['Body']

        sqs_client.delete_message(
            QueueUrl = queue_url,
            ReceiptHandle = message['ReceiptHandle']
        )

        print('Done')
        return body

def send_to_sqs(queue_name, message):
    # use environment variable for account_id & region (?)
    # send text of the bucket_path from where to take
    # for example:
    # bucket_name = brute-crawler
    # sqs text will be where you've put the file to "timestamp/start_url/brute-data.json"
    sqs_client = boto3.client('sqs')
    region, account_id = get_region_and_account_id()
    queue_url = f'https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}'
    sqs_client.send_message(
        QueueUrl = queue_url,
        MessageBody = message
    )

def upload_to_s3(bucket_name, file_path, worker_name):
    # worker name is also the name of the parent path in s3
    s3_client = boto3.client('s3')
    bucket_path = get_bucket_worker_bucket_path(file_path, worker_name)

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    encoded_data = json.dumps(json_data).encode(encode_type)

    s3_client.put_object(
        Body = encoded_data,
        Bucket = bucket_name,
        Key = bucket_path
    )

def upload_dict_to_s3(bucket_name, bucket_path, data):
    print(f'Uploading crawler data to {bucket_name} S3')
    s3_client = boto3.client('s3')
    encoded_data = json.dumps(data).encode(encode_type)

    s3_client.put_object(
        Body = encoded_data,
        Bucket = bucket_name,
        Key = bucket_path
    )
    print('Done')

def download_from_worker_s3(bucket_name, file_path, worker_name) -> dict:
    bucket_path = get_bucket_worker_bucket_path(file_path, worker_name)
    return download_from_s3(bucket_name, bucket_path)

def download_from_s3(bucket_name, bucket_path) -> dict:
    s3_client = boto3.client('s3')
    response = s3_client.get_object(
        Bucket = bucket_name,
        Key = bucket_path
    )
    return json.loads(response['Body'].read().decode(encode_type))