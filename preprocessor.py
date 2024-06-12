import pandas as pd
import re


def preprocess(data):
    # Define regex patterns for date and time
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?(?:AM|PM)?) - '

    # Split data into individual messages
    messages = re.split(pattern, data)[1:]

    # Initialize lists to store the parsed data
    dates, times, users, messages_content = [], [], [], []

    # Iterate over the messages and parse the content
    for i in range(0, len(messages) - 1, 3):
        date = messages[i]
        time = messages[i + 1]
        message = messages[i + 2]

        # Further split the message to extract user and message content
        if ": " in message:
            user, message_content = message.split(": ", 1)
        else:
            user, message_content = "group_notification", message

        dates.append(date)
        times.append(time)
        users.append(user)
        messages_content.append(message_content)

    # Create DataFrame
    df = pd.DataFrame({
        'date': pd.to_datetime(dates, format='%m/%d/%y'),
        'time': times,
        'user': users,
        'message': messages_content
    })

    # Additional preprocessing steps
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = pd.to_datetime(df['time'], format='%I:%M %p').dt.hour
    df['minute'] = pd.to_datetime(df['time'], format='%I:%M %p').dt.minute

    # Create 'period' column
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-0")
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df