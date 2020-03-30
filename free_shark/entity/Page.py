class Page:
    def __init__(self,**kwargs):
        self._current = kwargs.get('current',1)
        self._limit = kwargs.get('limit',6)
        self._rows = kwargs.get('rows',None)
        self._path = kwargs.get('path',None)

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self,new_current):
        self._current = new_current
    
    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self,new_limit):
        self._limit = new_limit

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self,new_rows):
        self._rows = new_rows

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,new_path):
        self._path = new_path

    # 得到当前页的起始行
    def get_offset(self):
        return (self._current-1)*self._limit
    
    # 得到页的总数
    def get_total(self):
        if self._rows % self._limit == 0:
            return self._rows / self._limit
        else:
            return int(self._rows / self._limit) + 1
    
    # 得到起始页
    def get_from(self):
        from_page = self._current - 2
        if from_page < 1:
            return 1
        else:
            return from_page
    
    # 得到最终页
    def get_to(self):
        to_page = self._current + 2
        total = self.get_total()
        if to_page > total:
            return total
        else:
            return to_page

    def get_list(self):
        l = []
        i = self.get_from()
        while i <= self.get_to():
            l.append(i)
            i = i + 1
        return l