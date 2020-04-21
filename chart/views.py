# encoding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from bitango.mongo.mongo_handle import MongoHandle
from chart.lib.paint import Paint


def chart_list(request):
    """
    图表列表
    :param request:
    :return:
    """
    return HttpResponse('chart list')

def chart_kline(request, instrument_id, rule):
    """
    图表详情
    :param request:
    :param rule: 重采样间隔时间
    :param instrument_id:
    :return:
    """
    instrument_id = 'BCH-USD-SWAP'
    result = MongoHandle.get_swap_from_time(instrument_id=instrument_id, as_df=False)
    # for item in result:
    #     print(item)

    template_name = 'kline.html'
    Paint.kline(result=result, file_name=template_name, title=instrument_id)

    context = {
    }
    return render(request, 'chart/paint/%s' % template_name, context=context)
