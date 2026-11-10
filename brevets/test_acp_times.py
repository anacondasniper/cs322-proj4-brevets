import acp_times

START = "2026-11-09T08:00:00-08:00"

def test_open_100_on_200():
    assert acp_times.open_time(100, 200, START) == '2026-11-09T10:56:00-08:00'

def test_open_350_on_400():
    assert acp_times.open_time(350, 400, START) == "2026-11-09T18:34:00-08:00"

def test_close_350_on_400():
    assert acp_times.close_time(350, 400, START) == "2026-11-10T07:20:00-08:00"

def test_open_890_on_1000():
    assert acp_times.open_time(890, 1000, START) == '2026-11-10T13:09:00-08:00'

def test_close_890_on_1000():
    assert acp_times.close_time(890, 1000, START) == '2026-11-12T01:23:00-08:00'

def test_close_0_on_200():
    assert acp_times.close_time(0, 200, START) == "2026-11-09T09:00:00-08:00"

def test_close_30_on_200():
    assert acp_times.close_time(30, 200, START) == "2026-11-09T10:30:00-08:00"
