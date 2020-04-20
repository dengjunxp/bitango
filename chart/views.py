from django.shortcuts import render
from django.http import HttpResponse


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

    # return HttpResponse(text)
    return render(request, 'chart/kline.html')
