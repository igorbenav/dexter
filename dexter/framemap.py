"""
FrameMap
---------
Data in the form of a dictionary of dataframes, the keys are the names of the dataframes.

"""
from typing import List
import pandas as pd
import numpy as np
from dexter.display import _to_html_str_, _to_html_
import dexter.optimizer


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

    # ------------ Constructors ------------

    def __init__(
            self,
            frames: List[pd.DataFrame],
            names: List[str] = []
    ):

        super().__init__()

        self.frames = frames
        self.names = names
        if not names:
            self.names = [str(i) for i in range(len(frames))]

        for frame, name in zip(frames, names):
            self[str(name)] = frame

    def __getattr__(self, key: str):
        return self.get(key)

    def __setattr__(self, key: str, value: pd.DataFrame) -> None:
        self[key] = value

    # ------------ Rendering Methods -------------

    def _repr_html_(self) -> str:
        """
        Return a HTML representation for a FrameMap
        """
        return _to_html_str_(self.frames, self.names)

    def display(self) -> 'IPython.core.display.HTML':
        """
        Receives a FrameMap.
        Returns a table which contains each IpyTable in an HTML cell.

        Returns
        -------
        IPython.core.display.HTML
        """

        return _to_html_(self.frames, self.names)

    # ------------ IO methods -------------

    def rename_frames(self, new_names: List[str]) -> None:
        """
        Renames the dataframes in a framemap by using a list of the new names
        if a new name is None, uses the old name

        Parameters
        ----------
        new_names : list[str], default None
        """
        # uses old name if new_name given is None
        new_names = [self.names[i] if not new_names[i] else new_names[i] for i in range(len(self.names))]

        for name, frame in zip(new_names, self.frames):
            if name in self.names:
                del self[name]

            self[name] = frame

        self.names = new_names

    def to_csv(self, names=None) -> None:
        """
        Receives a FrameMap
        Generates a csv file for each of the dataframes with its name.

        Parameters
        ----------
        names : list[str], default None
        """
        if not names:
            names = self.names

        for frame, name in zip(self.frames, names):
            frame.to_csv(name + '.csv')

    def to_excel(self, names=None) -> None:
        """
        Receives a FrameMap
        Generates a xlsx file for each of the dataframes with its name.

        Parameters
        ----------
        names : list[str], default None
        """
        if not names:
            names = self.names

        for frame, name in zip(self.frames, names):
            frame.to_excel(name + '.xlsx')

    def to_pickle(self, names=None) -> None:
        """
        Receives a FrameMap
        Generates a xlsx file for each of the dataframes with its name.

        Parameters
        ----------
        names : list[str], default None
        """
        if not names:
            names = self.names

        for frame, name in zip(self.frames, names):
            frame.to_pickle(name + '.pkl')

    def to_parquet(self, names=None) -> None:
        """
        Receives a FrameMap
        Generates a parquet file for each of the dataframes with its name.

        Parameters
        ----------
        names : list[str], default None
        """
        if not names:
            names = self.names

        for frame, name in zip(self.frames, names):
            frame.to_parquet(name + '.parquet')

    def optimize(self) -> 'FrameMap':
        """
        Receives a FrameMap
        Returns a FrameMap with all dataframes column types converted to the smallest possible type

        Returns
        -------
        FrameMap
        """
        return FrameMap([dexter.optimizer.optimize(df) for df in self.frames], self.names)

    @property
    def T(self) -> 'FrameMap':
        """
        transposes all dataframes in a FrameMap
        """
        return FrameMap([df.T for df in self.frames], self.names)

    # ------------ Statistical Methods -------------

    def dtypes(self) -> 'FrameMap':
        """
        Receives a FrameMap.
        Returns a list of dataframes with each showing the types of each column of each original
        dataframe.

        Returns
        -------
        FrameMap
        """
        df_types_list = []

        for df in self.frames:
            # checking the types of the columns
            df_types = df.dtypes

            # now an array with the columns names and values is created
            types_df = np.array((df_types.index, df_types.values))

            # finally, a dataframe is created out of this array and appended to the df_types_list
            df_types_list.append(pd.DataFrame([types_df[1]], columns=types_df[0], index=['type']))

        return FrameMap(df_types_list, self.names)

    def multiple_missing(self) -> 'FrameMap':
        """
        Receives FrameMap.

        Returns a list of dataframes with each showing the amount of missing values from each
        column of each original dataframe.

        Returns
        -------
        list[pd.DataFrame]
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

            return FrameMap(missing_values_df_list, self.names)

    def describe(self) -> 'FrameMap':
        """
        Receives a FrameMap.
        Returns a list of dataframes with each showing the types of each column of each original
        dataframe.

        Returns
        -------
        FrameMap
        """

        return FrameMap([df.describe(include='all') for df in self.frames], self.names)

    def head(self, n: int = 5) -> 'FrameMap':
        """
        Receives a FrameMap.
        Returns a table which contains each df.head(n) in an HTML cell.

        Parameters
        ----------
        n : int, default 5

        Returns
        -------
        FrameMap
        """

        return FrameMap([frame.head(n) for frame in self.frames], self.names)

    def tail(self, n: int = 5) -> 'FrameMap':
        """
        Receives a FrameMap.
        Returns a table which contains each df.tail(n).

        Parameters
        ----------
        n : int, default 5

        Returns
        -------
        FrameMap
        """
        return FrameMap([frame.tail(n) for frame in self.frames], self.names)

    def memory_usage(self) -> 'FrameMap':
        """
        Receives a FrameMap.
        Returns a table which contains each df.memory_usage(deep=True).

        Returns
        -------
        FrameMap
        """
        tables = []

        # appends dataframes out of total and each column's memory usage for each df in self
        for df, name in zip(self.frames, self.names):
            memory = df.memory_usage(deep=True)
            total = pd.Series(memory.sum(), index=[name])

            tables.append(pd.DataFrame(total.append(memory), columns=['Memory']))

        return FrameMap(tables, self.names)

    def shapes(self) -> 'FrameMap':
        """
        Receives a FrameMap.
        Returns a table which contains the shapes of each df.

        Returns
        -------
        FrameMap
        """

        # getting the shapes and names of each dataframe in self
        shapes_list = [df.shape for df in self.frames]
        names_list = list(self.names)

        shapes_df = pd.DataFrame(shapes_list, columns=['rows', 'columns'], index=names_list)

        return FrameMap([shapes_df], self.names)

    def nunique(self) -> 'FrameMap':
        """
        Receives a FrameMap.
        Returns a table which contains the number of non-null values of each column

        Returns
        -------
        FrameMap
        """

        # getting the count of nunique values for each dataframe in self
        return FrameMap([pd.DataFrame(df.nunique(), columns=['non-null']) for df in self.frames], self.names)

    def std(self, axis: int = None, skipna: bool = True, level: int = None, ddof: int = 1, numeric_only: bool = None) -> 'FrameMap':
        """
        Returns a FrameMap with all standard deviations

        Parameters
        ----------
        axis : {index (0), columns (1)}, default None
        skipna : bool, default True
            Exclude NA/null values. If an entire row/column is NA, the result will be NA.
        level : int or level name, default None
            If the axis is a MultiIndex (hierarchical), count along a particular level, collapsing into a Series.
        ddof : int, default 1
            Delta Degrees of Freedom. The divisor used in calculations is N - ddof, where N represents the number of
            elements.
        numeric_only : bool, default None
             Include only float, int, boolean columns. If None, will attempt to use everything, then use only numeric
             data.

        Returns
        -------
        FrameMap
            FrameMap with each standard deviation of dataframes.
        """
        return FrameMap(
            [pd.DataFrame(frame.std(axis, skipna, level, ddof, numeric_only), columns=['std']) for frame in self.frames],
            self.names
        )

    def mean(self, axis: int = None, skipna: bool = True, level: int = None, numeric_only: bool = None) -> 'FrameMap':
        """
        Returns the means for each dataframe in a framemap.

        Parameters
        ----------
        axis : int or None, default None
            the axis {index (0), columns (1)}
        skipna : bool, default True
            Exclude NA/null values. If an entire row/column is NA, the result will be NA.
        level : int or level name, default None
            If the axis is a MultiIndex (hierarchical), count along a particular level, collapsing into a Series.
        numeric_only : bool, default None
             Include only float, int, boolean columns. If None, will attempt to use everything, then use only numeric
             data.

        Returns
        -------
        FrameMap
            FrameMap with the means of each dataframe.
        """
        return FrameMap(
            [pd.DataFrame(frame.mean(axis, skipna, level, numeric_only), columns=['mean']) for frame in self.frames],
            self.names
        )

    def median(self, axis: int = None, skipna: bool = True, level: int = None, numeric_only: bool = None) -> 'FrameMap':
        """
        Returns the median for each dataframe in a framemap.

        Parameters
        ----------
        axis : int or None, default None
            the axis {index (0), columns (1)}
        skipna : bool, default True
            Exclude NA/null values. If an entire row/column is NA, the result will be NA.
        level : int or level name, default None
            If the axis is a MultiIndex (hierarchical), count along a particular level, collapsing into a Series.
        numeric_only : bool, default None
             Include only float, int, boolean columns. If None, will attempt to use everything, then use only numeric
             data.

        Returns
        -------
        FrameMap
            FrameMap with the medians of each dataframe.
        """
        return FrameMap(
            [pd.DataFrame(frame.median(axis, skipna, level, numeric_only), columns=['median']) for frame in self.frames],
            self.names
        )

    def mode(self, axis: int = 0, numeric_only: bool = None, dropna: bool = True):
        """
        Returns the mode for each dataframe in a framemap.

        Parameters
        ----------
        axis : int or None, default None
            the axis {index (0), columns (1)}
        numeric_only : bool, default None
             Include only float, int, boolean columns. If None, will attempt to use everything, then use only numeric
             data.
        dropna : bool, default True
                Don’t consider counts of NaN/NaT.

        Returns
        -------
        FrameMap
            FrameMap with the modes of each dataframes.
        """
        return FrameMap(
            [pd.DataFrame(frame.mode(axis, numeric_only, dropna), columns=['mode']) for frame in self.frames],
            self.names
        )

    def min(self, axis: int = None, skipna: bool = True, level: int = None, numeric_only: bool = None) -> 'FrameMap':
        """
        Returns the min values for each dataframe in a framemap.

        Parameters
        ----------
        axis : int or None, default None
            the axis {index (0), columns (1)}
        skipna : bool, default True
            Exclude NA/null values. If an entire row/column is NA, the result will be NA.
        level : int or level name, default None
            If the axis is a MultiIndex (hierarchical), count along a particular level, collapsing into a Series.
        numeric_only : bool, default None
             Include only float, int, boolean columns. If None, will attempt to use everything, then use only numeric
             data.

        Returns
        -------
        FrameMap
            FrameMap with the min values of each dataframes.
        """
        return FrameMap(
            [pd.DataFrame(frame.min(axis, skipna, level, numeric_only), columns=['min']) for frame in self.frames],
            self.names
        )

    def max(self, axis: int = None, skipna: bool = True, level: int = None, numeric_only: bool = None) -> 'FrameMap':
        """
        Returns the min values for each dataframe in a framemap.

        Parameters
        ----------
        axis : int or None, default None
            the axis {index (0), columns (1)}
        skipna : bool, default True
            Exclude NA/null values. If an entire row/column is NA, the result will be NA.
        level : int or level name, default None
            If the axis is a MultiIndex (hierarchical), count along a particular level, collapsing into a Series.
        numeric_only : bool, default None
             Include only float, int, boolean columns. If None, will attempt to use everything, then use only numeric
             data.

        Returns
        -------
        FrameMap
            FrameMap with the min values of each dataframes.
        """
        return FrameMap(
            [pd.DataFrame(frame.max(axis, skipna, level, numeric_only), columns=['max']) for frame in self.frames],
            self.names
        )

    def corr(self, method: str = 'pearson', min_periods: int = 1) -> 'FrameMap':
        """
        Compute pairwise correlation of columns for all dataframes excluding NA values.

        Parameters
        ----------
        method : {'pearson', 'kendall', 'spearman'} or callable
            Method of correlation used.
        min_periods : int
            Minimum number of observations per pair of columns.

        Returns
        -------
        FrameMap
            FrameMap of correlation matrices for dataframes.
        """
        return FrameMap(
            [frame.corr(method, min_periods) for frame in self.frames],
            self.names
        )

    # ------------ Reindexing Methods -------------

    def reset_index(self, level=None, drop=False, inplace=False, col_level=0, col_fill=''):
        """
        Reset the index, or a level of it.

        Reset the index of the DataFrame, and use the default one instead. If the DataFrame has a MultiIndex, this
        method can remove one or more levels.

        Parameters
        ----------
        level : int, str, tuple, or list, default None
            the levels to be removed from the index, removes all by default
        drop : bool, default False
            do not try to insert index into dataframe columns. This resets the index to the default integer index.
        inplace : bool, default False
            reset the indexes in place
        col_level : int or str, default 0
            If the columns have multiple levels, determines which level the labels are inserted into.
            By default it is inserted into the first level.
        col_fill : object, default ''
            If the columns have multiple levels, determines how the other levels are named. If None then the index name is repeated.

        Returns
        -------
        FrameMap or None
            FrameMap with each DataFrame with the new index or None if inplace=True.
        """
        out = None

        if inplace:
            for frame in self.frames:
                frame.reset_index(level, drop, inplace, col_level, col_fill)

        else:
            out = FrameMap([frame.reset_index(level, drop, inplace, col_level, col_fill) for frame in self.frames])

        return out
