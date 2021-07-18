from IPython.core.display import HTML


def to_html(df_list):
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

    return HTML(f'<tr>{tables}</tr>')
