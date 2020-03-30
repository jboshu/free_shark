from free_shark.statistics import Statistics
from datetime import datetime,timedelta

class UserStatistics(Statistics):

    def stat(self):
        sql="""
        CALL userRegisterStat(%s,%s);
        """

        try:
            self.cursor.execute(sql,(self.start_time,self.end_time))
            results=self.cursor.fetchall()
            return results
        except:
            self.db.rollback()
            raise
    