import pandas as pd
import numpy as np
import pytz

from qstrader.system.rebalance.rebalance import Rebalance


class WeeklyRebalance(Rebalance):
    """
    Generates a list of rebalance timestamps for pre- or post-market,
    for a particular trading day of the week between the starting and
    ending dates provided.

    All timestamps produced are set to UTC.

    Parameters
    ----------
    start_date : `pd.Timestamp`
        The starting timestamp of the rebalance range.
    end_date : `pd.Timestamp`
        The ending timestamp of the rebalance range.
    weekday : `str`
        The three-letter string representation of the weekday
        to rebalance on once per week.
    pre_market : `Boolean`, optional
        Whether to carry out the rebalance at market open/close.
    """

    def __init__(
        self,
        start_date,
        #end_date,
        weekday,
        pre_market=False
    ):
        self.weekdays = np.array(("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"))
        self.weekday = self._set_weekday(weekday)
        self.start_date = start_date
        #self.end_date = end_date
        self.pre_market_time = self.set_market_time(pre_market)
        #self.rebalances = self._generate_rebalances()

    def _set_weekday(self, weekday):
        """
        Checks that the weekday string corresponds to
        a business weekday.

        Parameters
        ----------
        weekday : `str`
            The three-letter string representation of the weekday
            to rebalance on once per week.

        Returns
        -------
        `str`
            The uppercase three-letter string representation of the
            weekday to rebalance on once per week.
        """
        weekday = weekday.upper()
        if weekday not in self.weekdays:
            raise ValueError(
                "Provided weekday keyword '%s' is not recognised "
                "or not a valid weekday." % weekday
            )

        result = np.where(self.weekdays == weekday)
        return result[0][0]



    # def _generate_rebalances(self):
    #     """
    #     Output the rebalance timestamp list.

    #     Returns
    #     -------
    #     `list[pd.Timestamp]`
    #         The list of rebalance timestamps.
    #     """
    #     rebalance_dates = pd.date_range(
    #         start=self.start_date,
    #         end=self.end_date,
    #         freq='W-%s' % self.weekday
    #     )

    #     rebalance_times = [
    #         pd.Timestamp(
    #             "%s %s" % (date, self.pre_market_time), tz=pytz.utc
    #         )
    #         for date in rebalance_dates
    #     ]

    #     return rebalance_times

    def is_rebalance_event(self, dt) -> bool:
        return dt >= self.start_date and self.weekday == dt.day_of_week and self.is_market_time(self.pre_market_time, dt)
    