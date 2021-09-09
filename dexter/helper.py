from IPython.core.display import HTML
from typing import List
import pandas as pd


def _to_html_str_(df_list: List[pd.DataFrame], name_list: List[str]):
    """
    Receives a list of dataframes and a list of names

    Returns a string of a html table with each dataframe side by side and the names above it
    """


    tables = (
        ''.join(
            ('<table><tr style="background-color:white;">',
             ''.join([f'<td style="vertical-align:top">' + f'<h5 style="text-align:center">{name}</h5><br>' +
                      table._repr_html_() + '</td>' for table, name in zip(df_list, name_list)]),
             '</tr></table>')
        )
    )

    return f'<tr>{tables}</tr>'


def _to_html_(df_list: List[pd.DataFrame], name_list: List[str]):
    """
    Receives a list of dataframes and a list of names

    Returns a html table with each dataframe side by side and the names above it
    """
    return HTML(_to_html_str_(df_list, name_list))
