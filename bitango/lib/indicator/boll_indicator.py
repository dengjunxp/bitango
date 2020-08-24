# encoding=utf-8

class BollIndicator:
    @classmethod
    def get_value(cls, df, median_rolling=20, coefficient=2):
        """
        计算布林带
        :param df:
        :param median_rolling: 中轨n根K线的移动平均线
        :param coefficient: 系数
        :return:
        """

        # 计算中轨
        df['boll_median'] = df['close'].rolling(median_rolling, min_periods=1).mean()

        # 计算标准差
        df['boll_std'] = df['close'].rolling(median_rolling, min_periods=1).std(ddof=0)  # ddof 标准差自由度

        # 计算上轨
        df['boll_upper'] = df['boll_median'] + coefficient * df['boll_std']

        # 计算下轨
        df['boll_lower'] = df['boll_median'] - coefficient * df['boll_std']

