from free_shark.resources.statistics_resource import StatResource
from free_shark.statistics.user_statistics import UserStatistics
from free_shark.resources.configs import Block_Stat_Fields

class UserRegisterStatResource(StatResource):
    def get_stat_obj(self):
        return UserStatistics
    
    def get_result_fields(self):
        return Block_Stat_Fields