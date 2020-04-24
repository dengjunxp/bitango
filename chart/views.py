# encoding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from bitango.mongo.mongo_handle import MongoHandle
from chart.lib.paint import Paint
from chart.lib.pandas_function import PandasFunction as pf
from bitango.lib.common import TimeOperation

def chart_list(request):
    """
    图表列表
    :param request:
    :return:
    """
    return HttpResponse('chart list')

def chart_kline(request, instrument_id, rule_type, start_time):
    """
    图表详情
    :param request:
    :param instrument_id: 币对（如：BCH-USD-SWAP）
    :param rule_type: 重采样间隔时间
    :param start_time: 开始时间（字符串，起始时间：2020-01-05 13:49:00，时间戳：1578203340）
    :return:
    """
    start_time = TimeOperation.string2timestamp(start_time, format_str='%Y-%m-%d %H:%M:%S')
    swap_df = MongoHandle.get_swap_from_time(instrument_id=instrument_id, start_time=start_time, as_df=True)

    # 重采样
    swap_df = pf.resample(df=swap_df, rule_type=rule_type)
    # 指标
    swap_df['ma7'] = swap_df['close'].rolling(7, min_periods=1).mean()
    # 画图
    template_name = 'kline.html'
    Paint.kline(result=swap_df, file_name=template_name, title=instrument_id, is_df=True)

    context = {
    }
    return render(request, 'chart/paint/%s' % template_name, context=context)
