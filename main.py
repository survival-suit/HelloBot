import datetime as dt
TIME_OFFSET = 3


def print_current_time():
    current_datetime = dt.datetime.utcnow() + dt.timedelta(hours=TIME_OFFSET)
    current_time = current_datetime.strftime("%H:%M")
    print(current_time)


if __name__ == '__main__':
    print_current_time()
