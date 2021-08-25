import pandas as pd
from typing import List


def optimize(df: pd.DataFrame, datetime_features: List[str] = None) -> pd.DataFrame:
    """
    Receives a dataframe
    Returns a dataframe with column types converted to the smallest possible type

    Parameters
    ----------
    df : pd.DataFrame
        the pandas dataframe to be optimized
    datetime_features : List[str] default None
        list of features that can be converted to datetime

    Returns
    -------
    pd.DataFrame
    """
    # avoiding mutable default variables
    datetime_features = datetime_features or []

    # converting float64 columns to the smallest possible precision
    floats = df.select_dtypes(include=['float64']).columns.tolist()
    df[floats] = df[floats].apply(pd.to_numeric, downcast='float')

    # converting int64 columns to the smallest possible precision
    ints = df.select_dtypes(include=['int64']).columns.tolist()
    df[ints] = df[ints].apply(pd.to_numeric, downcast='integer')

    # converting objects to categories or datetime objects
    for col in df.select_dtypes(include=['object']):
        if col not in datetime_features:
            num_unique_values = len(df[col].unique())
            num_total_values = len(df[col])
            if float(num_unique_values) / num_total_values < 0.5:
                df[col] = df[col].astype('category')
        else:
            df[col] = pd.to_datetime(df[col])

    return df
