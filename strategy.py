import backtrader as bt

class EMARSIATRStrategy(bt.Strategy):
    params = dict(
      fast_ema=20,
     slow_ema=50,
     rsi_period=14,
     rsi_buy=55,
     atr_period=14,
     risk_per_trade=0.02,
    )
   

    def __init__(self):
        self.fast_ema = bt.indicators.EMA(period=self.p.fast_ema)
        self.slow_ema = bt.indicators.EMA(period=self.p.slow_ema)
        self.cross = bt.indicators.CrossOver(self.fast_ema, self.slow_ema)

        self.rsi = bt.indicators.RSI(period=self.p.rsi_period)
        self.atr = bt.indicators.ATR(period=self.p.atr_period)

        self.order = None
        self.stop_price = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.cross > 0 and self.rsi > self.p.rsi_buy:
                cash = self.broker.get_cash()
                risk_amount = cash * self.p.risk_per_trade

                stop_distance = self.atr[0] * 2
                size = max(int(risk_amount / stop_distance), 1)

                self.stop_price = self.data.close[0] - stop_distance
                self.order = self.buy(size=size)

        else:
            if self.data.close[0] < self.stop_price or self.cross < 0:
                self.order = self.sell(size=self.position.size)

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            self.order = None