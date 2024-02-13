'''
Write a Code to read from a Master file (which contains a list of all file names), connect to S3 with each file name mentioned in the Master File, get the data from the bucket key and write it to Dynamodb

'''

import json
import boto3
import datetime

bucket_name = 'aws-bmo-podr'
# prefix = 'trigger-for-lambda-dynamodb'
# object_key = f'{prefix}/Main File.txt'


s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('table-example')

    
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
        elif 'Item' not in data:
            return {
                "success": 0,
                "data" : "No data found"

            }   
        else:
            return {
                "success": 3,
                "data" : "Error !!"

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
def read_from_s3(bucket, key):
    try:
        object = s3_client.get_object(Bucket=bucket_name, Key=key)
        body = object['Body'].read().decode('utf-8')
        return body
    except Exception as e:
        raise Exception(e)
def move_file_to_s3(local_file_path, bucket_name, s3_key):
    try:
        s3_client.upload_file(local_file_path, bucket_name, s3_key)
    
     except Exception as e:
        raise Exception(e)
   
def lambda_handler(event, context):
    
    response = []
    source_config_file_name = ''
    config_file_version = ''
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]
    source_config_file_name = object_key.split("/")[1]
    object = read_from_s3(bucket_name, object_key)
    source_file_data = object['Body'].read().decode('utf-8')
    source_file_data = json.loads(source_file_data)
    if "file_names" not in source_file_data:
        raise Exception("Error !! No key named file_names exist. The JSON should contain 'file_names' in array/list format ")
    if not isinstance(source_file_data['file_names'], list):
        raise Exception(("Error !! file_names is not a list/array"))
        
    config_file_names = source_file_data['file_names']   
    for fl in config_file_names:
        object_key_in_main_file = fl
        config_file_version = object_key_in_main_file.split("/")[2]
        # print(f"File Key = {object_key_in_main_file}")
        
        object_content = read_from_s3(bucket_name, object_key_in_main_file)
        
        file_content = object_content['Body'].read().decode('utf-8')
        
        config_file_values = json.loads(file_content)
        
        read_key = {
            'tbl_key': f"{config_file_values['tbl_key']}"
        }
        read_response = read_from_dynamodb_by_partitionkey(read_key)
        if read_response['success'] == 0:
            print(f"Success = {read_response['success']}, meaning INSERT NEW COLUMN")
            config_file_values["release_source_config_file"] = source_config_file_name
            config_file_values["config_file_version"] = config_file_version
            config_file_values["created_ts"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            config_file_values["updated_ts"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(f"Config File Values= {config_file_values}")
            resp = write_to_dynamodb(config_file_values)
            response.append(resp)
        elif read_response['success'] == 1:
            print(f"Success = {read_response['success']}, meaning UPDATE EXISTING COLUMN")
            update_expression = '''
                            SET tbl_name = :tbl_name_value, 
                            release_source_config_file = :release_source_config_file_value,
                            config_file_version = :config_file_version_value,
                            updated_ts = :updated_ts_value
                '''
            expression_attribute_values = {
                 ':tbl_name_value': config_file_values["tbl_name"],
                 ':release_source_config_file_value': source_config_file_name,
                 ':config_file_version_value': config_file_version,
                 ':updated_ts_value': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            }
            print(f"Update Exp = {update_expression}")
            print("\n")
            print(f"Expression Attribute Values = {expression_attribute_values}")
            # raise Exception("lsgrelgore")
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
        
