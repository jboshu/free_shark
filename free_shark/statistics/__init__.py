from free_shark.db import get_db_with_dict_cursor
from datetime import datetime,timedelta

class Statistics(object):
    def __init__(self,start_time=None,end_time=None):
        super().__init__()
        self.db=get_db_with_dict_cursor()
        self.cursor=self.db.cursor()
        if start_time is None:
            self.start_time=datetime.now()
        else:
            self.start_time=start_time
        if end_time is None:
            self.end_time=self.start_time+timedelta(days=7)  
        else:
            self.end_time=end_time
    
    def stat(self):
        raise NotImplementedError