'''
Write a Code to read from a Master file (which contains a list of all file names), connect to S3 with each file name mentioned in the Master File, get the data from the bucket key and write it to Dynamodb
'''

import json
import boto3

bucket_name = 'aws-bmo-podr'
prefix = 'trigger-for-lambda-dynamodb'
object_key = f'{prefix}/Main File.txt'
response = []

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('table-example')

item_to_add = {
        'tbl_key ': 'tbl_1',
        'tbl_name': 'AB'
    }
    
def write_to_dynamodb(item):
    try:
        table.put_item(Item=item)
        return "Item added successfully"
    except Exception as e:
        return e
    
def read_from_dynamodb_by_partitionkey(item):
    try:
        data = table.get_item(
                Key = item
        )
        
        if 'Item' in data['Item']:
            return data['Item']
        else:
            "No data found"
       
    except Exception as e:
        return e
    
   
def lambda_handler(event, context):
    # bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    # object_key = event["Records"][0]["s3"]["object"]["key"]
    
    object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    body = object['Body'].read().decode('utf-8')
    file_name = body.split('\r\n')
    for fl in file_name:
        object_key_in_main_file = f"{prefix}/{fl}"
        print(f"File Key = {object_key_in_main_file}")
        object_content = s3_client.get_object(Bucket=bucket_name, Key=object_key_in_main_file)
        file_content = object_content['Body'].read().decode('utf-8')
        print(f"File Content in {fl} file = {file_content} ")
        data_to_write = json.loads(file_content)
        resp = write_to_dynamodb(data_to_write)
        response.append(resp)
        
    
    # data_to_write = json.loads(body)
    # print(body)
    # response = read_from_dynamodb_by_partitionkey(item1)
    
    # response = write_to_dynamodb(data_to_write)
    # response = body
    print(response)
    return response
        
    
    