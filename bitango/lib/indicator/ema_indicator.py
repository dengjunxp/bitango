# encoding=utf-8

import talib as ta


class EmaIndicator:
    @classmethod
    def get_value(cls, df, ema_name):
        """
        计算指数移动平均线指标
        :param df:
        :param ema_name:
        :return:
        """
        ma_num = int(ema_name.replace('ma', ''))
        if ma_num <= 0:
            return
        df[ema_name] = df['close'].rolling(ma_num, min_periods=1).mean()
