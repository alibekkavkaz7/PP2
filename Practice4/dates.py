from datetime import datetime, timedelta

# 1. five days from current date
now = datetime.now()
five_days_ago = now - timedelta(days=5)
print("Five days ago:", five_days_ago)


# 2. yesterday, today, tomorrow
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)


# 3. microseconds
current_time = datetime.now()
no_microseconds = current_time.replace(microsecond=0)
print("Without microseconds:", no_microseconds)


# 4. difference between two dates in seconds
date1 = datetime(2024, 1, 1)
date2 = datetime(2024, 1, 10)

difference = date2 - date1
print("Difference in seconds:", difference.total_seconds())
