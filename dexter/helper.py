from IPython.core.display import HTML
# TODO: Document better parameters and return types such as def function(parameter: type) -> return type


def _to_html_str_(df_list):
    """
    Receives a list of dataframes

    Returns a html table with each dataframe side by side
    """
    tables = (
        ''.join(
            ('<table><tr style="background-color:white;">',
             ''.join([f'<td style="vertical-align:top">' + table._repr_html_() + '</td>' for table in df_list]),
             '</tr></table>')
        )
    )

    return f'<tr>{tables}</tr>'


def _to_html_(df_list):
    """
    Receives a list of dataframes

    Returns a html table with each dataframe side by side
    """
    return HTML(_to_html_str_(df_list))
