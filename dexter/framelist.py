"""
FrameList
---------
Data in the form of a list of dataframes.

"""

from dexter.display import _to_html_str_


class FrameList(list):
    """
    Data in the form of a list of dataframes.

    Parameters
    ----------
    frames: List containing pandas dataframes.

    Example
    -------
    >>> dataframes = FrameList([df1, df2, df3])
    >>> dataframes
    FrameList([df1, df2, df3])
    _______
    """

    def _repr_html_(self) -> str:
        """
        Return a HTML representation for a FrameList
        """
        return _to_html_str_(self)
