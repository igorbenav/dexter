import numpy as np
import pandas as pd
import os
from dexter.framelist import FrameList


def readm_csv(filepath, df_names=None):
    """
    Read multiple files in a directory, returns a FrameList
    If df_names == None, it iterates the whole directory.

    Receives the path and optionally a list of the dataframes names.

    Returns a FrameList

    the folder should have only csv files, no .txt
    """
    df_list = []

    # Here the function uses the names of the dataframes to read the files
    if df_names is not None:
        df_names = np.char.array(df_names)
        filepath = np.full(df_names.shape, filepath)
        reader = filepath + df_names + '.csv'

        temp_df = [pd.read_csv(i) for i in reader]
        df_list.append(temp_df)

    # If names are not given, the function just reads all data in folder
    else:
        df_names = []
        path, dirs, files = next(os.walk(filepath))
        file_count = len(files)
        for i in range(file_count):
            temp_df = pd.read_csv(filepath + files[i])
            df_list.append(temp_df)
            df_names.append(files[i][:-4])

    return FrameList(df_list, df_names)
