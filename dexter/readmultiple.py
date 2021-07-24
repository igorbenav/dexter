import numpy as np
import pandas as pd
import os
from dexter.framemap import FrameMap
from typing import List
# TODO: optimize before appending to df_list


def read_chunks(df_chunk) -> pd.DataFrame:
    """
    Reads a chunks object of a pandas dataframe

    Receives the object of a pd.read with chunksize smaller than the size of the dataset

    Returns the dataframe
    """
    chunk_list = []

    for chunk in df_chunk:
        # chunk_filter = chunk_preprocessing(chunk)
        # chunk_list.append(chunk_filter)
        chunk_list.append(chunk)

    df = pd.concat(chunk_list)

    return df


def readm_csv(filepath: str, df_names: List[str] = None, chunksize: int = None, optimize: bool = False) -> FrameMap:
    """
    Reads multiple files in a directory, returns a FrameMap
    If df_names == None, it iterates the whole directory.
    If optimize == True, returns a memory optimized version

    Receives the path and optionally a list of the dataframes names.

    Returns a FrameMap

    the folder should have only csv files, no .txt
    """
    df_list = []

    # Here the function uses the names of the dataframes to read the files
    if df_names is not None:
        df_names = np.char.array(df_names)
        filepath = np.full(df_names.shape, filepath)
        reader = filepath + df_names + '.csv'

        temp_df = [pd.read_csv(i, chunksize=chunksize) for i in reader]
        df_list.append(temp_df)

    # If names are not given, the function just reads all data in folder
    else:
        df_names = []
        path, dirs, files = next(os.walk(filepath))
        file_count = len(files)
        for i in range(file_count):
            temp_df = pd.read_csv(filepath + files[i], chunksize=chunksize)
            df_list.append(temp_df)
            df_names.append(files[i][:-4])

    # If chunk_size is given, df_list is actually a list of reader objects,
    # Let's unpack these objects
    if chunksize is not None:
        df_list = [read_chunks(i) for i in df_list]

    framemap = FrameMap(df_list, df_names)

    # return memory optimized version if selected
    if optimize:
        framemap = framemap.optimize()

    return framemap


def readm_json(filepath: str, df_names: List[str] = None, chunksize: int = None, optimize: bool = False) -> FrameMap:
    """
    Reads multiple files in a directory, returns a FrameMap
    If df_names == None, it iterates the whole directory.
    If optimize == True, returns a memory optimized version

    Receives the path and optionally a list of the dataframes names.

    Returns a FrameMap

    the folder should have only json files, no .txt
    """
    df_list = []

    # Here the function uses the names of the dataframes to read the files
    if df_names is not None:
        df_names = np.char.array(df_names)
        filepath = np.full(df_names.shape, filepath)
        reader = filepath + df_names + '.json'

        temp_df = [pd.read_json(i, chunksize=chunksize) for i in reader]
        df_list.append(temp_df)

    # If names are not given, the function just reads all data in folder
    else:
        df_names = []
        path, dirs, files = next(os.walk(filepath))
        file_count = len(files)
        for i in range(file_count):
            temp_df = pd.read_json(filepath + files[i], chunksize=chunksize)
            df_list.append(temp_df)
            df_names.append(files[i][:-5])

    # If chunk_size is given, df_list is actually a list of reader objects,
    # Let's unpack these objects
    if chunksize is not None:
        df_list = [read_chunks(i) for i in df_list]

    framemap = FrameMap(df_list, df_names)

    # return memory optimized version if selected
    if optimize:
        framemap = framemap.optimize()

    return framemap


def readm_excel(filepath: str, df_names: List[str] = None, chunksize: int = None, optimize: bool = False) -> FrameMap:
    """
    Reads multiple files in a directory, returns a FrameMap
    If df_names == None, it iterates the whole directory.
    If optimize == True, returns a memory optimized version

    Receives the path and optionally a list of the dataframes names.

    Returns a FrameMap

    the folder should have only xlsx files, no .txt
    """
    df_list = []

    # Here the function uses the names of the dataframes to read the files
    if df_names is not None:
        df_names = np.char.array(df_names)
        filepath = np.full(df_names.shape, filepath)
        reader = filepath + df_names + '.xlsx'

        temp_df = [pd.read_excel(i, chunksize=chunksize) for i in reader]
        df_list.append(temp_df)

    # If names are not given, the function just reads all data in folder
    else:
        df_names = []
        path, dirs, files = next(os.walk(filepath))
        file_count = len(files)
        for i in range(file_count):
            temp_df = pd.read_excel(filepath + files[i], chunksize=chunksize)
            df_list.append(temp_df)
            df_names.append(files[i][:-5])

    # If chunk_size is given, df_list is actually a list of reader objects,
    # Let's unpack these objects
    if chunksize is not None:
        df_list = [read_chunks(i) for i in df_list]

    framemap = FrameMap(df_list, df_names)

    # return memory optimized version if selected
    if optimize:
        framemap = framemap.optimize()

    return framemap
