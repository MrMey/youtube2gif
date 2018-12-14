import logging
import re
import datetime

import url_checker

class Gif:
    def __init__(self, id):
        self._url = ""
        self._start_time = ""
        self._stop_time = ""
        self.id = id
        self._metadata = {}

    def get_url(self):
        return(self._url)

    def set_url(self,url):
        if not url_checker.is_valid_root_url(url):
            logging.error("invalid url")
            raise ValueError("url is not a proper Youtube url")

        self._url = url
    url = property(get_url,set_url)

    def get_metadata(self):
        return self._metadata

    def set_metadata(self,meta_data):
        self._metadata = meta_data
    metadata = property(get_metadata,set_metadata)

    def get_start_time(self):
        return self._start_time
    
    def set_start_time(self,start_time = "00:00:00"):
        if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$", start_time):
            if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])\.([0-9]{0,3})$", start_time):
                logging.error("start time has not the right format")
                raise ValueError("start time has not the right format")
            else:
                self._start_time = datetime.datetime.strptime(start_time,"%H:%M:%S.%f").time()
        else:
            self._start_time = datetime.datetime.strptime(start_time,"%H:%M:%S").time()
    start_time = property(get_start_time, set_start_time)

    def get_stop_time(self):
        return self._stop_time
    
    def set_stop_time(self,stop_time = "00:00:00"):
        if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$", stop_time):
            if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])\.([0-9]{0,3})$", stop_time):
                logging.error("start time has not the right format")
                raise ValueError("start time has not the right format")
            else:
                self._stop_time = datetime.datetime.strptime(stop_time,"%H:%M:%S.%f").time()
        else:
            self._stop_time = datetime.datetime.strptime(stop_time,"%H:%M:%S").time()
        
        if self._stop_time <= self._start_time:
            logging.error("stop time is smaller than start time")
            raise ValueError("stop time is smaller than start time")
    stop_time = property(get_stop_time, set_stop_time)
