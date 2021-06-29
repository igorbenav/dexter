"""
FrameList
---------
Data in the form of a list of two tuples, one containing the names of dataframes and
other containing the dataframes themselves.

"""

import pandas as pd
import numpy as np
from IPython.core.display import HTML


class FrameList:
    """
    Data in the form of a list of two tuples, one containing the names of dataframes and
    other containing the dataframes themselves.

    Parameters
    ----------
    frames: List containing pandas dataframes.

    names : list of strings or None, default None
        List containing the names of the dataframes.
        If names is None, range(len(frames))

    Example
    -------
    >>> dataframes = FrameList([df1, df2, df3], ['df1_name', 'df2_name', 'df3_name'])
    >>> dataframes
    [('df1_name', 'df2_name', 'df3_name'),
    (df1, df2, df3)]
    """
    # @property
    # def _constructor(self) -> type(FrameList):
    #     return FrameList

    # ------------ Constructors ------------

    def __init__(
            self,
            frames,
            names=None
    ):

        self.frames = frames
        self.names = names
        if names is None:
            self.names = range(len(frames))

    def dtypes(self):
        """
        Receives a FrameList.

        Returns a list of dataframes with each showing the types of each column of each original
        dataframe.
        """
        df_types_list = []

        for df in self.frames:
            # checking the types of the columns
            df_types = df.dtypes

            # now an array with the columns names and values is created
            types_df = np.array((df_types.index, df_types.values))

            # finally, a dataframe is created out of this array and appended to the df_types_list
            df_types_list.append(pd.DataFrame([types_df[1]], columns=types_df[0], index=['type']))

        return df_types_list

    def multiple_missing(self):
        """
        Receives FrameList.

        Returns a list of dataframes with each showing the amount of missing values from each
        column of each original dataframe.
        """
        missing_values_df_list = []

        for df in self.frames:
            # computing and storing missing values
            df_missing_values = df.isnull().sum()

            # now an array with the columns names and values is created
            missing_values_df = np.array((df_missing_values.index, df_missing_values.values))

            # finally, a dataframe is created out of this array and appended to the missing_values_list
            missing_values_df_list.append(
                pd.DataFrame([missing_values_df[1]], columns=missing_values_df[0], index=['missing']))

        return missing_values_df_list

    def describe(self):
        """
        Receives a FrameList.

        Returns a list of dataframes with each showing the types of each column of each original
        dataframe.
        """
        df_descriptions_list = []

        for df in self.frames:
            # checking the types of the columns
            df_descriptions = df.describe(include='all')

            # finally, a dataframe is created out of this array and appended to the df_types_list
            df_descriptions_list.append(df_descriptions)

        return df_descriptions_list

    def display(self):
        """
        Receives a FrameList .

        Returns a table which contains each IpyTable in an HTML cell.

        Notes
        -----
        TODO: show the names of each dataframe above it in the future
        """
        table_names = [''.join(f'<th style="text-align:center">{name}</th>') for name in self.names]
        tables = (
            ''.join(
                ('<table><tr style="background-color:white;">',
                 ''.join([f'<td style="vertical-align:top">' + table._repr_html_() + '</td>' for table in self.frames]),
                 '</tr></table>')
            )
        )

        return HTML(f'<tr>{tables}</tr>')

    def head(self, n=5):
        """
        Receives a FrameList

        Returns a table which contains each df.head(n) in an HTML cell.
        """
        heads = [frame.head(n) for frame in self.frames]
        tables = (
            ''.join(
                ('<table><tr style="background-color:white;">',
                 ''.join([f'<td style="vertical-align:top">' + table._repr_html_() + '</td>' for table in heads]),
                 '</tr></table>')
            )
        )

        return HTML(f'<tr>{tables}</tr>')

    def tail(self, n=5):
        """
        Receives a FrameList

        Returns a table which contains each df.tail(n) in an HTML cell.
        """
        heads = [frame.tail(n) for frame in self.frames]
        tables = (
            ''.join(
                ('<table><tr style="background-color:white;">',
                 ''.join([f'<td style="vertical-align:top">' + table._repr_html_() + '</td>' for table in heads]),
                 '</tr></table>')
            )
        )

        return HTML(f'<tr>{tables}</tr>')

    def memory_usage(self):
        """
        Receives a FrameList

        Returns a table which contains each df.memory_usage(deep=True) in an HTML cell.
        """
        tables = []

        for df, name in zip(self.frames, self.names):
            memory = df.memory_usage(deep=True)
            total = pd.Series(memory.sum(), index=[name])

            df = pd.DataFrame(total.append(memory), columns=['Memory'])

            tables.append(df)

        tables = (
            ''.join(
                ('<table><tr style="background-color:white;">',
                 ''.join([f'<td style="vertical-align:top">' + table._repr_html_() + '</td>' for table in tables]),
                 '</tr></table>')
            )
        )

        return HTML(f'<tr>{tables}</tr>')
