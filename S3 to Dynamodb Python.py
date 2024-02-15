'''
Write a Code to read from a Master file (which contains a list of all file names), connect to S3 with each file name mentioned in the Master File, get the data from the bucket key and write it to Dynamodb

'''

import json
import boto3
import datetime
import os

bucket_name = os.environ["bucket_name"]
# print(f"Bucket Name = {bucket_name}")
# raise Exception("elghwu")
# prefix = 'trigger-for-lambda-dynamodb'
# object_key = f'{prefix}/Main File.txt'


s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_files = 'table-example-2'
table_events = 'table-example'
dynamodb_config_folders = [
    'file-configs' ,
    'event-configs'
]
dynamodb_table_mappings = {
    dynamodb_config_folders[0]: table_files,
    dynamodb_config_folders[1]: table_events,
}

target_s3_key_for_event_object = "config-files/event-config-backup"
target_s3_key_for_files_object = "config-files/file-config-backup"
target_s3_key_for_release_config = "op-source-config-backup"

def write_to_dynamodb(table,item):
    try:
        table.put_item(Item=item)
        return "Item added successfully"
    except Exception as e:
        return e
    
def read_from_dynamodb_by_partitionkey(table,item):
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
def update_to_dynamodb(table,item, update_expression, expression_attribute_values):
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
        object = s3_client.get_object(Bucket=bucket, Key=key)
        body = object['Body'].read().decode('utf-8')
        return body
    except Exception as e:
        raise Exception(e)
def copy_file_to_s3(bucket_name, source_key, target_key):
    try:
        s3_client.copy_object(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'Key': source_key},
            Key=target_key
        )
    
    except Exception as e:
        raise Exception(e)
def delete_file_from_s3(bucket_name, object_key):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)
    
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
    source_file_data = json.loads(object)
    read_key = {}

    
    if "file_names" not in source_file_data:
        raise Exception("Error !! No key named file_names exist. The JSON should contain 'file_names' in array/list format ")
    if not isinstance(source_file_data['file_names'], list):
        raise Exception("Error !! file_names is not a list/array")
        
    config_file_names = source_file_data['file_names']   
    for object_key_in_main_file in config_file_names:
   
        config_file_version = object_key_in_main_file.split("/")[2]
        folder_location = object_key_in_main_file.split("/")[1]
        table = dynamodb.Table(dynamodb_table_mappings[folder_location])
        print(f"File Key = {object_key_in_main_file}")
        # continue
        
        object_content = read_from_s3(bucket_name, object_key_in_main_file)
        config_file_values = json.loads(object_content)
        # print(f"folder_location = {folder_location} , Config File Values = {config_file_values}")
        # continue
        if folder_location == dynamodb_config_folders[0]: # folder_loc = file-configs
            
            read_key = {
                'file_id': f"{config_file_values['file_id']}"
            }
        elif folder_location == dynamodb_config_folders[1]: # folder_loc = event-configs
            
            read_key = {
                'event_id': f"{config_file_values['event_id']}"
            }
        else:
             raise Exception(f"Folder Location Name {folder_location} must be one of the following {dynamodb_config_folders}")
        read_response = read_from_dynamodb_by_partitionkey(table,read_key)
        if read_response['success'] == 0:
            print(f"Success = {read_response['success']}, meaning INSERT NEW COLUMN")
            config_file_values["release_source_config_file"] = source_config_file_name
            config_file_values["config_file_version"] = config_file_version
            config_file_values["created_ts"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            config_file_values["updated_ts"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(f"Config File Values = {config_file_values}")
            resp = write_to_dynamodb(table,config_file_values)
            if folder_location == dynamodb_config_folders[0]: # folder_loc = file-configs
                copy_file_to_s3(bucket_name, object_key_in_main_file, target_s3_key_for_files_object)
                
            elif folder_location == dynamodb_config_folders[1]:  # folder_loc = event-configs
                copy_file_to_s3(bucket_name, object_key_in_main_file, target_s3_key_for_event_object)
            delete_file_from_s3(bucket_name, object_key_in_main_file)
            response.append(resp)
           
        elif read_response['success'] == 1:
            print(f"Success = {read_response['success']}, meaning UPDATE EXISTING ROW")
            if folder_location == dynamodb_config_folders[0]: # folder_loc = file-configs
                update_expression = 'SET '
                if 'payment_type' in config_file_values:
                    update_expression += 'payment_type = :payment_type_value,'
                if 'config_value' in config_file_values:
                    update_expression += 'config_value = :config_value,'
                update_expression += ' release_source_config_file = :release_source_config_file_value, config_file_version = :config_file_version_value,updated_ts = :updated_ts_value'
                    
                expression_attribute_values = {}
                if 'payment_type' in config_file_values:
                    expression_attribute_values[':payment_type_value'] = config_file_values["payment_type"] 
                if 'config_value' in config_file_values:
                    expression_attribute_values[':config_value'] = config_file_values["config_value"]  
                    
                expression_attribute_values[':release_source_config_file_value'] = source_config_file_name
                expression_attribute_values[':config_file_version_value'] = config_file_version
                expression_attribute_values[':updated_ts_value'] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                   
                print(f"File Loop :- Update Exp = {update_expression}")
                print("\n")
                print(f"Expression Attribute Values = {expression_attribute_values}")
                # raise Exception("lsgrelgore")
                resp = update_to_dynamodb(table, read_key, update_expression, expression_attribute_values)
                copy_file_to_s3(bucket_name, object_key_in_main_file, target_s3_key_for_files_object)
                delete_file_from_s3(bucket_name, object_key_in_main_file)
                response.append(resp)
            elif folder_location == dynamodb_config_folders[1]:  # folder_loc = event-configs
                update_expression = 'SET '
                if 'tbl_name' in config_file_values:
                    update_expression += 'tbl_name = :tbl_name_value,'
                if 'config_value' in config_file_values:
                    update_expression += 'config_value = :config_value,'
                update_expression += ' release_source_config_file = :release_source_config_file_value, config_file_version = :config_file_version_value,updated_ts = :updated_ts_value'
                    
                expression_attribute_values = {}
                if 'tbl_name' in config_file_values:
                    expression_attribute_values[':tbl_name_value'] = config_file_values["tbl_name"] 
                if 'config_value' in config_file_values:
                    expression_attribute_values[':config_value'] = config_file_values["config_value"]  
                    
                expression_attribute_values[':release_source_config_file_value'] = source_config_file_name
                expression_attribute_values[':config_file_version_value'] = config_file_version
                expression_attribute_values[':updated_ts_value'] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                   
                # update_expression = '''
                #                 SET tbl_name = :tbl_name_value, 
                #                 release_source_config_file = :release_source_config_file_value,
                #                 config_file_version = :config_file_version_value,
                #                 updated_ts = :updated_ts_value
                #     '''
                # expression_attribute_values = {
                #     ':tbl_name_value': config_file_values["tbl_name"],
                #     ':release_source_config_file_value': source_config_file_name,
                #     ':config_file_version_value': config_file_version,
                #     ':updated_ts_value': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                # }
                print(f"Event Loop :- Update Exp = {update_expression}")
                print("\n")
                print(f"Expression Attribute Values = {expression_attribute_values}")
                # raise Exception("lsgrelgore")
                resp = update_to_dynamodb(table,read_key, update_expression, expression_attribute_values)
                copy_file_to_s3(bucket_name, object_key_in_main_file, target_s3_key_for_event_object)
                delete_file_from_s3(bucket_name, object_key_in_main_file)
                response.append(resp)
                
                
            else:
                raise Exception(f"Folder Location Name {folder_location} must be one of the following {dynamodb_config_folders}")
        else:
            resp = read_response['data']
            response.append(resp)
    copy_file_to_s3(bucket_name, object_key, target_s3_key_for_release_config)
    delete_file_from_s3(bucket_name, object_key)
    
            

    
    print(response)
    return response
        
