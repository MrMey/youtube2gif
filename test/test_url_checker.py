import sys
sys.path.append("..")

import url_checker

def test_url():
    assert not url_checker.is_valid_root_url("bla")
    assert url_checker.is_valid_root_url("https://www.youtube.com/watch?v=9GkVhgIeGJQ&start_radio=1&list=RDEMLUGe1lzhB7MnQLLEheFTww")
test_url()