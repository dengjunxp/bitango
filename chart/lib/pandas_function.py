# encoding=utf-8

import pandas as pd


class PandasFunction(object):

    @classmethod
    def resample(cls, df, rule_type=5):
        """
        重采样
        :param df:
        :param rule_type: （如：5T 5分钟K线）
        :return:
        """
        period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
        })

        period_df.dropna(subset=['open'], inplace=True)
        period_df = period_df[period_df['volume'] > 0]
        period_df.reset_index(inplace=True)
        df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]
        return df

    @classmethod
    def display_init(cls):
        """
        初始化pandas参数
        :return:
        """
        # 不换行显示
        pd.set_option('expand_frame_repr', False)
        # pd.set_option('display.max_rows', 100)
        # pd.set_option('display.min_rows', 100)
        pd.set_option('display.max_rows', None)
