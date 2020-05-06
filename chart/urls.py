# encoding=utf-8
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart_list),
    # 图表
    # http://127.0.0.1:9000/chart/kline/BCH-USD-SWAP/5T/2020-01-05%2014:55:00/
    path('kline/<instrument_id>/<rule_type>/<start_time>/', views.chart_kline),

    # macd
    # http://127.0.0.1:9000/chart/kline_macd/BCH-USD-SWAP/5T/2020-01-05%2014:55:00/
    path('kline_macd/<instrument_id>/<rule_type>/<start_time>/', views.chart_macd),
]
