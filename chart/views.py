from django.shortcuts import render
from django.http import HttpResponse
from bitango.mongo.mongo_handle import MongoHandle
from django.conf import settings


def chart_list(request):
    """
    图标列表
    :param request:
    :return:
    """
    return HttpResponse('chart list')

def chart_kline(request, instrument_id, rule):
    """
    图标详情
    :param request:
    :param rule: 重采样间隔时间
    :param instrument_id:
    :return:
    """
    instrument_id = 'BCH-USD-SWAP'
    # result = MongoHandle.get_swap_from_time(instrument_id=instrument_id, as_df=False)
    # print(result)
    return HttpResponse('hello world')
    # return render(request, 'chart/kline.html')
