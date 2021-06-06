from qstrader.system.rebalance.rebalance import Rebalance


class BuyAndHoldRebalance(Rebalance):
    """
    Generates a single rebalance timestamp at the start date in
    order to create a single set of orders at the beginning of
    a backtest, with no further rebalances carried out.

    Parameters
    ----------
    start_dt : `pd.Timestamp`
        The starting datetime of the buy and hold rebalance.
    """

    def __init__(self, start_dt):
        self.start_dt = start_dt
        self.pre_market_time = self.set_market_time(False)
        #self.rebalances = [start_dt]

    def is_rebalance_event(self, dt):
        return dt >= self.start_dt and self.is_market_time(self.pre_market_time, dt)
