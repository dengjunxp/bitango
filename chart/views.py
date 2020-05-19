# encoding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from bitango.mongo.mongo_handle import MongoHandle
from chart.lib.paint.kline import PaintKline
from chart.lib.paint.kline_macd import PaintKlineMacd

from chart.lib.pandas_function import PandasFunction as pf
from bitango.lib.common import TimeOperation

from bitango.lib.indicator.macd_indicator import MacdIndicator
from bitango.lib.indicator.rsi_indicator import RsiIndicator
from bitango.lib.indicator.ema_indicator import EmaIndicator

pf.display_init()


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
    # 公司数据起始时间：2020-01-05 13:49:00
    # 转时间戳
    start_time = TimeOperation.string2timestamp(start_time)
    swap_df = MongoHandle.get_swap_from_time(instrument_id=instrument_id, start_time=start_time, as_df=True)

    # 重采样
    swap_df = pf.resample(df=swap_df, rule_type=rule_type)
    # 指标
    swap_df['ma20'] = swap_df['close'].rolling(20, min_periods=1).mean()
    # 画图
    template_name = 'kline.html'
    # 指标的索引位置
    indicator_index = {
        'ma20': 6,
    }
    render_embed = PaintKline.paint(result=swap_df, file_name=template_name, title=instrument_id, is_df=True,
                                    indicator_index=indicator_index)
    return HttpResponse(render_embed)

    # 从文件中读取模板
    # template_path = Paint.kline(result=swap_df, file_name=template_name, title=instrument_id, is_df=True,
    #                             indicator_index=indicator_index)
    # context = {
    # }
    # return render(request, template_path, context=context)


def chart_macd(request, instrument_id, rule_type, start_time):
    """
    MACD图形
    :param request:
    :param instrument_id:
    :param rule_type:
    :param start_time:
    :return:
    """
    # 公司数据起始时间：2020-01-05 13:49:00
    # 转换成时间戳
    start_time = TimeOperation.string2timestamp(start_time)
    swap_df = MongoHandle.get_swap_from_time(instrument_id=instrument_id, start_time=start_time, as_df=True)

    # 重采样
    swap_df = pf.resample(df=swap_df, rule_type=rule_type)

    # 指标
    # 极值
    swap_df['extremum'] = 0
    # MACD[7:9]
    MacdIndicator.get_value(swap_df)
    # RSI6[10]
    RsiIndicator.get_value(df=swap_df, rsi_name='rsi6')
    # EMA144[11]
    EmaIndicator.get_value(df=swap_df, ema_name='ema144')

    # 去除开头行的NaN
    # print(swap_df)
    swap_df.dropna(axis=0, how='any', inplace=True)

    # 转换为列表
    swap_arr = swap_df.values.tolist()
    for item in swap_arr:
        # datatime 转 string
        item[0] = TimeOperation.datetime2string(item[0])
        # high 和 close 交换
        temp = item[2]
        item[2] = item[4]
        item[4] = temp
        # dif、dea、macd 交换成 macd、dif、dea
        # 7    8    9
        temp = item[9]
        item[9] = item[8]
        item[8] = item[7]
        item[7] = temp

    # print(swap_arr)
    # print(type(swap_arr))
    # 画图
    # template_name = 'kline.html'
    # # 指标的索引位置
    # indicator_index = {
    #     # 'ma20': 6,
    # }
    # render_embed = PaintKline.paint(result=swap_df, file_name=template_name, title=instrument_id, is_df=True,
    #                                 indicator_index=indicator_index)
    # return HttpResponse(render_embed)

    render_embed = PaintKlineMacd.paint(echarts_data=swap_arr)
    return HttpResponse(render_embed)

