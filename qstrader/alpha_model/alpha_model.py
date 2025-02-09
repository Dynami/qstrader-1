from abc import ABCMeta, abstractmethod
from qstrader.asset.universe.universe import Universe
from qstrader.signals.signals_collection import SignalsCollection


class AlphaModel(object):
    """
    Abstract interface for an AlphaModel callable.

    A derived-class instance of AlphaModel takes in an Asset
    Universe and an optional DataHandler instance in order
    to generate forecast signals on Assets.

    These signals are used by the PortfolioConstructionModel
    to generate target weights for the portfolio.

    Implementing __call__ produces a dictionary keyed by
    Asset and with a scalar value as the signal.
    """

    __metaclass__ = ABCMeta

    def __init__(self, signals:SignalsCollection) -> None:
        self.signals = signals

    @abstractmethod
    def __call__(self, dt, universe:Universe):
        raise NotImplementedError(
            "Should implement __call__()"
        )
