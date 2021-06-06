from abc import ABCMeta, abstractmethod


class Rebalance(object):
    """
    Interface to a generic list of system logic and
    trade order rebalance timestamps.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def is_rebalance_event(self, dt) -> bool:
        raise NotImplementedError(
            "Should implement is_rebalance_event()"
        )
    
    def set_market_time(self, pre_market:bool):
        """
        Determines whether to use market open or market close
        as the rebalance time.

        Parameters
        ----------
        pre_market : `Boolean`
            Whether to use market open or market close
            as the rebalance time.

        Returns
        -------
        `str`
            The string representation of the market time.
        """
        #return "14:30:00" if pre_market else "21:00:00"
        return (14, 30, 0) if pre_market else (21, 0, 0)

    def is_market_time(self, market_time, dt) -> bool:
        return dt.hour == market_time[0] and dt.minute == market_time[1] and dt.second == market_time[2]



    # @abstractmethod
    # def output_rebalances(self):
    #     raise NotImplementedError(
    #         "Should implement output_rebalances()"
    #     )
