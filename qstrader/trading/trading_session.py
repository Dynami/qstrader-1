from abc import ABCMeta, abstractmethod
from qstrader.exchange.exchange import Exchange
from qstrader.broker.fee_model.fee_model import FeeModel
from qstrader.asset.universe.universe import Universe
from qstrader import data
from qstrader.alpha_model.alpha_model import AlphaModel
from qstrader.data.backtest_data_handler import DataHandler
from qstrader.risk_model.risk_model import RiskModel


class TradingSession(object):
    """
    Interface to a live or backtested trading session.
    """

    #__metaclass__ = ABCMeta

    def __init__(self, 
        universe:Universe, 
        alpha_model:AlphaModel, 
        risk_model:RiskModel, 
        fee_model:FeeModel,
        exchange:Exchange
    ) -> None:
        self.universe = universe
        self.alpha_model = alpha_model
        self.risk_model = risk_model
        self.fee_model = fee_model,
        self.exchange = exchange

        #self.data_handler = data_handler


    @abstractmethod
    def run(self):
        raise NotImplementedError(
            "Should implement run()"
        )
