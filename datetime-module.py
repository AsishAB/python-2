import datetime

# Unix timestamp
timestamp = 1549244364

# Convert the timestamp to a datetime object
dt_object = datetime.datetime.fromtimestamp(timestamp)

# Extract day, month, year, hour, minute, and second
day = dt_object.day
month = dt_object.month
year = dt_object.year
hour = dt_object.hour
minute = dt_object.minute
second = dt_object.second

print("Day:", day)
print("Month:", month)
print("Year:", year)
print("Hour:", hour)
print("Minute:", minute)
print("Second:", second)
