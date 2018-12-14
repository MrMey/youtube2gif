import sys
sys.path.append("..")

import gif

def test_start_time():
    a = gif.Gif("0")
    a.set_start_time("00:00:03")
    a.set_stop_time("00:00:05")

    try:
        a.set_stop_time("00:00:02")
    except ValueError:
        assert True
    
test_start_time()