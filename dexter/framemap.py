"""
FrameMap
---------
Data in the form of a dictionary of dataframes, the keys are the names of the dataframes.

"""

import pandas as pd
import numpy as np
from dexter.framelist import FrameList
from dexter.helper import _to_html_str_, _to_html_


class FrameMap(dict):
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
    >>> dataframes = FrameMap([df1, df2, df3], ['df1_name', 'df2_name', 'df3_name'])
    >>> dataframes
    _______
    """
    # @property
    # def _constructor(self) -> type(FrameMap):
    #     return FrameMap

    # ------------ Constructors ------------

    def __init__(
            self,
            frames,
            names=None
    ):

        super().__init__()

        self.frames = frames
        self.names = names
        if names is None:
            self.names = range(len(frames))

        for frame, name in zip(frames, names):
            self[str(name)] = frame

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

    def _repr_html_(self):
        """
        Return a HTML representation for a FrameMap
        """
        return _to_html_str_(self.frames)

    def dtypes(self):
        """
        Receives a FrameMap.

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

        return FrameList(df_types_list)

    def multiple_missing(self):
        """
        Receives FrameMap.

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

        return FrameList(missing_values_df_list)

    def describe(self):
        """
        Receives a FrameMap.

        Returns a list of dataframes with each showing the types of each column of each original
        dataframe.
        """

        return FrameList([df.describe(include='all') for df in self.frames])

    def display(self):
        """
        Receives a FrameMap.

        Returns a table which contains each IpyTable in an HTML cell.

        Notes
        -----
        TODO: show the names of each dataframe above it
        """
        # unused for now, will be used to show the names of each dataframe above it
        table_names = [''.join(f'<th style="text-align:center">{name}</th>') for name in self.names]

        # creates an html representation of the tables side by side

        return _to_html_(self.frames)

    def head(self, n=5):
        """
        Receives a FrameMap.

        Returns a table which contains each df.head(n) in an HTML cell.
        """

        return FrameList([frame.head(n) for frame in self.frames])

    def tail(self, n=5):
        """
        Receives a FrameMap.

        Returns a table which contains each df.tail(n).
        """
        return FrameList([frame.tail(n) for frame in self.frames])

    def memory_usage(self):
        """
        Receives a FrameMap.

        Returns a table which contains each df.memory_usage(deep=True).
        """
        tables = []

        # appends dataframes out of total and each column's memory usage for each df in self
        for df, name in zip(self.frames, self.names):
            memory = df.memory_usage(deep=True)
            total = pd.Series(memory.sum(), index=[name])

            tables.append(pd.DataFrame(total.append(memory), columns=['Memory']))

        return FrameList(tables)

    def shapes(self):
        """
        Receives a FrameMap.

        Returns a table which contains the shapes of each df.
        """

        # getting the shapes and names of each dataframe in self
        shapes_list = [df.shape for df in self.frames]
        names_list = list(self.names)

        shapes_df = pd.DataFrame(shapes_list, columns=['rows', 'columns'], index=names_list)

        return FrameList([shapes_df])

    def nunique(self):
        """
        Receives a FrameMap.

        Returns a table which contains the number of non-null values of each column
        """

        # getting the count of nunique values for each dataframe in self
        return FrameList([pd.DataFrame(df.nunique(), columns=['non-null']) for df in self.frames])
