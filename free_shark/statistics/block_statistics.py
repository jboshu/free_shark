from free_shark.statistics import Statistics

class BlockStartStatistics(Statistics):
    def stat(self):
        sql="""
        CALL blockStartStat(%s,%s)
        """

        try:
            self.cursor.execute(sql,(self.start_time,self.end_time))
            results=self.cursor.fetchall()
            return results
        except:
            self.db.rollback()
            raise

class BlockEndStatistice(Statistics):
       def stat(self):
        sql="""
        CALL blockEndStat(%s,%s)
        """

        try:
            self.cursor.execute(sql,(self.start_time,self.end_time))
            results=self.cursor.fetchall()
            return results
        except:
            self.db.rollback()
            raise

class BlockDuringStatistics(Statistics):
        
    def stat(self):
        sql="""
        SELECT
            count(*) as count,
            DATE(start_time) as start_time,
            DATE(end_time) as end_time
        FROM
            block
        WHERE
            start_time > %s
        OR end_time < %s
        GROUP BY
            DATE(start_time),
            DATE(end_time)
        ORDER BY
	        start_time ASC
        """

        try:
            self.cursor.execute(sql,(self.start_time,self.end_time))
            results=self.cursor.fetchall()
            return results
        except:
            self.db.rollback()
            raise