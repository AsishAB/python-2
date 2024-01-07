import mysql.connector

# Establishing the connection
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='test_db',
        user='root',
        password='asish2442'
    )

    f = open('test-query.sql', 'r')
    f.seek(0)  # --> 0 means from the start of the file
    print("\n")
    query = f.read()
    print(query)
    f.close()

    # exit()
    if connection.is_connected():
        print('Connected to MySQL database')

        # Creating a cursor object using the cursor() method
        cursor = connection.cursor()

        
        # Executing the query
        cursor.execute(query)

        # Fetching all rows from the result set
        rows = cursor.fetchall()

        # Displaying the fetched data
        for row in rows:
            print(row)

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    # Closing the connection
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print('MySQL connection is closed')
