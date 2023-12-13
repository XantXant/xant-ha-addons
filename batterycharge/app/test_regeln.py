import time

def test_day_1():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 5, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 10, 16)

    assert start == time.mktime((2023, 12, 2, 10, 0, 0, 0, 0, 0))
    assert end == time.mktime((2023, 12, 2, 16, 0, 0, 0, 0, 0))

def test_day_2():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 12, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 10, 16)

    assert start == time.mktime((2023, 12, 2, 10, 0, 0, 0, 0, 0))
    assert end == time.mktime((2023, 12, 2, 16, 0, 0, 0, 0, 0))

def test_day_3():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 10, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 10, 16)

    assert start == time.mktime((2023, 12, 2, 10, 0, 0, 0, 0, 0))
    assert end == time.mktime((2023, 12, 2, 16, 0, 0, 0, 0, 0))

def test_day_4():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 16, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 10, 16)

    assert start == time.mktime((2023, 12, 3, 10, 0, 0, 0, 0, 0))
    assert end == time.mktime((2023, 12, 3, 16, 0, 0, 0, 0, 0))

def test_day_5():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 17, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 10, 16)

    assert start == time.mktime((2023, 12, 3, 10, 0, 0, 0, 0, 0))
    assert end == time.mktime((2023, 12, 3, 16, 0, 0, 0, 0, 0))

def test_overnight_1():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 2, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 20, 6)

    assert start == time.mktime((2023, 12, 1, 20, 0, 0, 0, 0, 0))
    assert end == time.mktime((2023, 12, 2, 6, 0, 0, 0, 0, 0))

def test_overnight_2():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 6, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 20, 6)

    assert start == (time.mktime((2023, 12, 2, 20, 0, 0, 0, 0, 0)))
    assert end == (time.mktime((2023, 12, 3, 6, 0, 0, 0, 0, 0)))

def test_overnight_3():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 12, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 20, 6)

    assert start == (time.mktime((2023, 12, 2, 20, 0, 0, 0, 0, 0)))
    assert end == (time.mktime((2023, 12, 3, 6, 0, 0, 0, 0, 0)))

def test_overnight_4():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 20, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 20, 6)

    assert start == (time.mktime((2023, 12, 2, 20, 0, 0, 0, 0, 0)))
    assert end == (time.mktime((2023, 12, 3, 6, 0, 0, 0, 0, 0)))

def test_overnight_5():
    from regeln import getstartendtime

    tst = time.mktime((2023, 12, 2, 22, 0, 0, 0, 0, 0))
    start, end = getstartendtime(tst, 20, 6)

    assert start == (time.mktime((2023, 12, 2, 20, 0, 0, 0, 0, 0)))
    assert end == (time.mktime((2023, 12, 3, 6, 0, 0, 0, 0, 0)))