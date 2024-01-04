'''
Write a python script that takes file name as input and generate a Redshift Query and store that query in a new file

'''





import re
import time
#
# schema = 'sch_shopping'
# table = ' tbl_cust'
# syntax = f'CREATE TABLE {schema}.{table} ('
#
# with open('sample.txt', 'r') as file:
#     for line in file:
#         line = re.sub(r'\s+', ' ', line)
#         line = line.replace(' ', ',')
#         line = line.split(",")
#         if (line.length == 2):
#             syntax += line[]
#
# Read data from the file

schema_name = 'online_shopping'
table_name = 'tbl_shoppers'
temp_file_name = 'tmp_file.txt'
create_table_sql = f'CREATE TABLE "{schema_name}"."{table_name}" (\n'
f = open(f'{table_name}.txt', 'r')
f.seek(0)
file_details = f.read()

file_details = re.sub(r'VARCHAR2\((\d+) CHAR\)', r'VARCHAR2(\1)', file_details)
file_details = file_details.replace("NOT NULL", "NOTNULL")       
file_details = re.sub(r'TIMESTAMP\(\d+\)', 'TIMESTAMP', file_details)

f = open(temp_file_name, 'w')
f.write(file_details)
# print(file_details)
f.close()
time.sleep(2)

with open(temp_file_name, 'r') as file:
    # columns = []
    for line in file:
        
        # print(line)
        line = re.sub(r'\s+', ' ', line)
        # line = re.sub(r'VARCHAR2\((\d+),\s*CHAR\)', r'VARCHAR2(\1 CHAR)', line)
        words = line.split()
        

        # Remove trailing spaces only from the last word
        last_word = words[-1].rstrip()

        # Reconstruct the sentence with the updated last word
        line = ' '.join(words[:-1] + [last_word])
        words = line.split()
        # print(words)
        # components = re.split(r'\s+', line)
        
        # # Modify the components if needed
        # if len(components) == 3 and components[2].endswith('CHAR)'):
        #     components[2] = components[2].replace('CHAR)', ')')
        
        # print(components)
        # print(len(words))
        if len(words) == 3:
            create_table_sql += "\t" + words[0] + " " + words[2] + " " + words[1] + ",\n"
        elif len(words) == 2:
            # words[1] = re.sub(r'VARCHAR2', 'character varying', words[1])
            create_table_sql += "\t" + words[0] + " " + words[1] + ",\n"


create_table_sql = re.sub(r'VARCHAR2\((\d+)\)', r'character varying(\1)', create_table_sql)
create_table_sql = create_table_sql.replace("NOTNULL", "NOT NULL")
create_table_sql = create_table_sql.replace("TIMESTAMP", "TIMESTAMP WITHOUT TIME ZONE")

create_table_sql = re.sub(r'NUMBER\((\d+)\)', r'INTEGER', create_table_sql)
create_table_sql = re.sub(r'NUMBER\((\d+),\s*(\d+)\)', r'DECIMAL(\1, \2)', create_table_sql)
create_table_sql = create_table_sql[:create_table_sql.rfind(',')] + create_table_sql[create_table_sql.rfind(',') + 1:]
create_table_sql += ")"
print(create_table_sql)

