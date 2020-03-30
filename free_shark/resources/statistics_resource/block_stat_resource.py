from flask_restful import Resource,reqparse,fields, marshal_with
from free_shark.resources.configs import Block_Stat_Fields,Block_During_Stat_Fields
from free_shark.resources.statistics_resource import StatResource
from free_shark.statistics.block_statistics import BlockDuringStatistics,BlockStartStatistics,BlockEndStatistice

class BlockDuringStatResource(StatResource):
    def get_stat_obj(self):
        return BlockDuringStatistics
    
    def get_result_fields(self):
        return Block_During_Stat_Fields

class BlockStartStatResource(StatResource):
    def get_stat_obj(self):
        return BlockStartStatistics

    def get_result_fields(self):
        return Block_Stat_Fields
    
class BlockEndStatResource(StatResource):
    def get_stat_obj(self):
        return BlockEndStatistice

    def get_result_fields(self):
        return Block_Stat_Fields

