# encoding=utf-8

import time
import pandas as pd
from pymongo import MongoClient
from bitango.lib.common import NetOperation

class MongoHandle:
    _client = None

    @classmethod
    def get_conf(cls):
        net_segment = NetOperation.get_net_segment()
        if net_segment in ['192.168.10', '192.168.0']:
            return ['192.168.10.10', '27017']

        elif net_segment in ['192.168.2']:
            return ['192.168.2.110', '27017']

    @classmethod
    def get_instance(cls):
        if cls._client is None:
            cls._client = cls.get_mongo_handler()
        return cls._client

    @classmethod
    def get_mongo_handler(cls):
        host, port = cls.get_conf()
        db_name = ''

        uri = 'mongodb://{host}:{port}/{db_name}?authSource={auth_source}' \
            .format(host=host, port=port, db_name=db_name, auth_source=db_name)
        client = MongoClient(uri)
        return client

    @classmethod
    def get_spot_collection(cls, collection_name):
        """
        获取现货数据库的连接
        :param collection_name:
        :return:
        """
        client = cls.get_instance()
        database = client['okex_spot']
        return database[collection_name]

    @classmethod
    def get_swap_collection(cls, collection_name):
        """
        获取合约数据库的连接
        :param collection_name:
        :return:
        """
        client = cls.get_instance()
        database = client['okex_swap']
        return database[collection_name]

    @classmethod
    def get_swap_from_time(cls, instrument_id, start_time=0, end_time=0, kline_length=2 * 24 * 60, as_df=True):
        """
        从数据库中获取合约数据（默认倒序）
        :param instrument_id:
        :param start_time: 开始时间戳
        :param end_time: 结束时间戳（下不包含）
        :param kline_length: K线数据的分钟数（默认2天）
        :param as_df: 获取结果后，是否转换成DataFrame
        :return:
        """
        result = []
        limit = 0
        time_sort = 1
        collection = cls.get_swap_collection(instrument_id)

        # 判断查询条件和返回条数
        if start_time != 0 and end_time != 0:
            condition = {"time": {"$gte": int(start_time), "$lt": int(end_time)}}
        elif start_time != 0:
            condition = {"time": {"$gte": int(start_time)}}
            limit = kline_length
        elif end_time != 0:
            condition = {"time": {"$lt": int(end_time)}}
            limit = kline_length
            time_sort = -1
        else:
            # 没有开始结束时间，则end_time为当前时间戳
            end_time = int(time.time())
            condition = {"time": {"$lt": int(end_time)}}
            limit = kline_length
            time_sort = -1

        temp = collection.find(condition).sort([('time', time_sort)])
        if limit > 0:
            temp = temp.limit(limit)
        # 添加结果
        for item in temp:
            result.append({
                'candle_begin_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['time'])),
                'open': float(item['open']),
                'high': float(item['high']),
                'low': float(item['low']),
                'close': float(item['close']),
                'volume': float(item['volume']),
            })
        if time_sort == -1:
            result = list(reversed(result))

        # 判断是否需要转换成DataFrame
        if as_df:
            df = pd.DataFrame(result)
            df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], format='%Y-%m-%d %H:%M:%S')
            return df
        return result

