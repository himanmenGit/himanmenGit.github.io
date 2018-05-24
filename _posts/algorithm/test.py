import datetime


def solution(a, b):
    t = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

    return t[datetime.date(2016, a, b).weekday()]


solution(5, 24)
