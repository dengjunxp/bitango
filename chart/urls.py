# encoding=utf-8
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart_list),
    # 图表
    path('detail/<instrument_id>/<interval>/', views.chart_detail)
]
