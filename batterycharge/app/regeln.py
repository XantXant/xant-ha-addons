import datetime
import time

def getstartendtime(act, start_hour, end_hour):
    act_time = datetime.datetime.fromtimestamp(act)
    start_time =  time.mktime((act_time.year, act_time.month, act_time.day, start_hour, 0, 0, 0, 0, 0))
    end_time =  time.mktime((act_time.year, act_time.month, act_time.day, end_hour, 0, 0, 0, 0, 0))

    # print("\nact", datetime.datetime.fromtimestamp(act), "start", datetime.datetime.fromtimestamp(start_time), "end", datetime.datetime.fromtimestamp(end_time))

    day = datetime.timedelta(days=1).total_seconds()

    if start_time < end_time:
        if act >= end_time:
            start_time += day
            end_time += day
    else:
        if act < start_time:
            if act < end_time:
                start_time -= day
            else:
                end_time += day
        else:
            if end_time < start_time:
                end_time += day

    # print("\nact", datetime.datetime.fromtimestamp(act), "start", datetime.datetime.fromtimestamp(start_time), "end", datetime.datetime.fromtimestamp(end_time))

    return start_time, end_time

if __name__ == "__main__":
    tst = datetime.datetime.now().timestamp()
    tst = time.mktime((2023, 12, 1, 2, 0, 0, 0, 0, 0))
    print(getstartendtime(tst, 20, 6))