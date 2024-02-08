'''
Write a Code to read from a Master file (which contains a list of all file names), connect to S3 with each file name mentioned in the Master File, get the data from the bucket key and write it to Dynamodb

'''

import json
import boto3

bucket_name = 'aws-bmo-podr'
prefix = 'trigger-for-lambda-dynamodb'
object_key = f'{prefix}/Main File.txt'


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
        
        if 'Item' in data:
            return {
                "success": 1,
                "data" : data['Item']

            }
        else:
            return {
                "success": 0,
                "data" : "No data found"

            }       
    except Exception as e:
        return {
                "success": 2,
                "data" : e

            }
def update_to_dynamodb(item, update_expression, expression_attribute_values):
    try:
        update_response = table.update_item(
            Key=item,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='UPDATED_NEW'
        )

        return f"Update Item succeeded: {update_response}"
    except Exception as e:
        return e
   
def lambda_handler(event, context):
    response = []
    
    # bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    # object_key = event["Records"][0]["s3"]["object"]["key"]
    
    object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    body = object['Body'].read().decode('utf-8')
    file_name = body.split('\r\n')
    for fl in file_name:
        object_key_in_main_file = f"{prefix}/{fl}"
        # print(f"File Key = {object_key_in_main_file}")
        object_content = s3_client.get_object(Bucket=bucket_name, Key=object_key_in_main_file)
        file_content = object_content['Body'].read().decode('utf-8')
        # print(f"File Content in {fl} file = {file_content} ")
        data = json.loads(file_content)
       
        read_key = {
            'tbl_key': f"{data['tbl_key']}"
        }
        read_response = read_from_dynamodb_by_partitionkey(read_key)
        if read_response['success'] == 0:
            print(f"Success = {read_response['success']}, meaning READ")
            resp = write_to_dynamodb(data)
            response.append(resp)
        elif read_response['success'] == 1:
            print(f"Success = {read_response['success']}, meaning WRITE")
            update_expression = 'SET tbl_name = :new_value, table_id = :new_value2'
            expression_attribute_values = {
                 ':new_value': 'Helofknwlejnre_21321y2349',
                 ':new_value2': '12312423432'
            }
            resp = update_to_dynamodb(read_key, update_expression, expression_attribute_values)
            response.append(resp)
        else:
            resp = read_response['data']
            response.append(resp)
            

        # Specify the update expression and attribute values
        # 
        # 
        # response.append(resp)
        
    
    # data_to_write = json.loads(body)
    # print(body)
    # response = read_from_dynamodb_by_partitionkey(item1)
    
    # response = write_to_dynamodb(data_to_write)
    
    print(response)
    return response
        
    
    
