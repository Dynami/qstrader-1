from abc import ABCMeta, abstractmethod
from qstrader.system.rebalance.rebalance import Rebalance
from qstrader.system.rebalance.end_of_month import EndOfMonthRebalance
from qstrader.system.rebalance.weekly import WeeklyRebalance
from qstrader.system.rebalance.daily import DailyRebalance
from qstrader.system.rebalance.buy_and_hold import BuyAndHoldRebalance
from qstrader.system.qts import QuantTradingSystem
from build.lib.qstrader.broker.broker import Broker
from qstrader.exchange.exchange import Exchange
from qstrader.broker.fee_model.fee_model import FeeModel
from qstrader.asset.universe.universe import Universe
from qstrader import data
from qstrader.alpha_model.alpha_model import AlphaModel
from qstrader.data.backtest_data_handler import DataHandler
from qstrader.risk_model.risk_model import RiskModel
import pandas as pd

class TradingSession(object):
    """
    Interface to a live or backtested trading session.
    """

    __metaclass__ = ABCMeta

    def __init__(self, 
        start_dt:pd.Timestamp,
        universe:Universe, 
        alpha_model:AlphaModel, 
        risk_model:RiskModel,
        broker:Broker,
        portfolio_id:str,
        long_only:bool,
        rebalance:str,
        rebalance_weekday:str=None,
        **kwargs
        
    ) -> None:
        self.start_dt = start_dt
        self.universe = universe
        self.alpha_model = alpha_model
        self.risk_model = risk_model
        self.broker = broker
        self.portfolio_id = portfolio_id
        self.long_only = long_only
        self.rebalance = rebalance
        self.rebalance_weekday = rebalance_weekday

        if rebalance == 'weekly' and rebalance_weekday is None:
            raise ValueError(
                "Rebalance frequency was set to 'weekly' but no specific "
                "weekday was provided. Try adding the 'rebalance_weekday' "
                "keyword argument to the instantiation of "
                "BacktestTradingSession, e.g. with 'WED'."
            )
        
        self.rebalance_schedule = self._create_rebalance_event_times()
        #self.qst = self._create_quant_trading_system(**kwargs)
        
    
    @abstractmethod
    def run(self):
        raise NotImplementedError(
            "Should implement run()"
        )

    def ___create_quant_trading_system(self, **kwargs):
        """
        Creates the quantitative trading system with the provided
        alpha model.

        TODO: All portfolio construction/optimisation is hardcoded for
        sensible defaults.

        Returns
        -------
        `QuantTradingSystem`
            The quantitative trading system.
        """
        if self.long_only:
            if 'cash_buffer_percentage' not in kwargs:
                raise ValueError(
                    'Long only portfolio specified for Quant Trading System '
                    'but no cash buffer percentage supplied.'
                )
            cash_buffer_percentage = kwargs['cash_buffer_percentage']
            print('trading_session.py', self.risk_model)
            qts = QuantTradingSystem(
                self.universe,
                self.broker,
                self.portfolio_id,
                self.alpha_model,
                self.risk_model,
                long_only=self.long_only,
                cash_buffer_percentage=cash_buffer_percentage,
                submit_orders=True
            )
        else:
            if 'gross_leverage' not in kwargs:
                raise ValueError(
                    'Long/short leveraged portfolio specified for Quant '
                    'Trading System but no gross leverage percentage supplied.'
                )
            gross_leverage = kwargs['gross_leverage']

            qts = QuantTradingSystem(
                self.universe,
                self.broker,
                self.portfolio_id,
                self.alpha_model,
                self.risk_model,
                long_only=self.long_only,
                gross_leverage=gross_leverage,
                submit_orders=True
            )

        return qts

    def _create_rebalance_event_times(self)-> Rebalance :
        """
        Creates the list of rebalance timestamps used to determine when
        to execute the quant trading strategy throughout the backtest.

        Returns
        -------
        `List[pd.Timestamp]`
            The list of rebalance timestamps.
        """
        if self.rebalance == 'buy_and_hold':
            rebalancer = BuyAndHoldRebalance(self.start_dt)
        elif self.rebalance == 'daily':
            rebalancer = DailyRebalance(self.start_dt)
        elif self.rebalance == 'weekly':
            rebalancer = WeeklyRebalance(self.start_dt, self.rebalance_weekday)
        elif self.rebalance == 'end_of_month':
            rebalancer = EndOfMonthRebalance(self.start_dt)
        else:
            raise ValueError(
                'Unknown rebalance frequency "%s" provided.' % self.rebalance
            )
        return rebalancer #.rebalances