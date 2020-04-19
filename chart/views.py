from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def chart_list(request):
    """
    图标列表
    :param request:
    :return:
    """
    return HttpResponse('chart list')

def chart_detail(request, instrument_id, interval):
    """
    图标详情
    :param request:
    :param interval: 重采样间隔时间
    :param instrument_id:
    :return:
    """
    text = 'visiting instrument: %s | %s ' % (interval, instrument_id)
    # return HttpResponse(text)
    return render(request, 'test.html')
