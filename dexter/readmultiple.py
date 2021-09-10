import numpy as np
import pandas as pd
import os
from dexter.framemap import FrameMap
from typing import List
# TODO: optimize before appending to df_list


def _read_chunks_(df_chunk) -> pd.DataFrame:
    """
    Reads a chunks object of a pandas dataframe
    Receives the object of a pd.read with chunksize smaller than the size of the dataset

    Returns the dataframe
    """
    chunk_list = [chunk for chunk in df_chunk]
    df = pd.concat(chunk_list)

    return df


def readm_csv(filepath: str, df_names: List[str] = None, chunksize: int = None, optimize: bool = False) -> FrameMap:
    """
    Reads multiple files in a directory, returns a FrameMap
    If df_names == None, it iterates the whole directory.
    If optimize == True, returns a memory optimized version

    Receives the path and optionally a list of the dataframes names.

    Returns a FrameMap

    Parameters
    ----------
    filepath : str
        the path of the folder to be read
    df_names : List[str], default None
        a list with the names of the files
    chunksize : int, default None
        an integer to read the files in chunks
    optimize : bool, default False
        if True, returns memory optimized version of dataframes

    Returns
    -------
    FrameMap
    """
    df_list = []

    # Here the function uses the names of the dataframes to read the files
    if df_names is not None:
        df_names = np.char.array(df_names)
        filepath = np.full(df_names.shape, filepath)
        reader = filepath + df_names + '.csv'

        df_list = [pd.read_csv(i, chunksize=chunksize) for i in reader]

    # If names are not given, the function just reads all data in folder
    else:
        df_names = []
        path, dirs, files = next(os.walk(filepath))
        # only files with the .csv extension matter
        files = [file for file in files if os.path.splitext(file)[-1] == '.csv']

        for file in files:
            temp_df = pd.read_csv(filepath + file, chunksize=chunksize)
            df_list.append(temp_df)
            df_names.append(file)

    # If chunk_size is given, df_list is actually a list of reader objects,
    # Let's unpack these objects
    if chunksize is not None:
        df_list = [_read_chunks_(i) for i in df_list]

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

    Parameters
    ----------
    filepath : str
        the path of the folder to be read
    df_names : List[str], default None
        a list with the names of the files
    chunksize : int, default None
        an integer to read the files in chunks
    optimize : bool, default False
        if True, returns memory optimized version of dataframes

    Returns
    -------
    FrameMap
    """
    df_list = []

    # Here the function uses the names of the dataframes to read the files
    if df_names is not None:
        df_names = np.char.array(df_names)
        filepath = np.full(df_names.shape, filepath)
        reader = filepath + df_names + '.json'

        df_list = [pd.read_json(i, chunksize=chunksize) for i in reader]

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
        df_list = [_read_chunks_(i) for i in df_list]

    framemap = FrameMap(df_list, df_names)

    # return memory optimized version if selected
    if optimize:
        framemap = framemap.optimize()

    return framemap


def readm_excel(filepath: str, df_names: List[str] = None, optimize: bool = False) -> FrameMap:
    """
    Reads multiple files in a directory, returns a FrameMap
    If df_names == None, it iterates the whole directory.
    If optimize == True, returns a memory optimized version

    Receives the path and optionally a list of the dataframes names.

    Returns a FrameMap

    the folder should have only xlsx files, no .txt

    Parameters
    ----------
    filepath : str
        the path of the folder to be read
    df_names : List[str], default None
        a list with the names of the files
    optimize : bool, default False
        if True, returns memory optimized version of dataframes

    Returns
    -------
    FrameMap
    """
    df_list = []

    # Here the function uses the names of the dataframes to read the files
    if df_names is not None:
        df_names = np.char.array(df_names)
        filepath = np.full(df_names.shape, filepath)
        reader = filepath + df_names + '.xlsx'

        df_list = [pd.read_excel(i) for i in reader]

    # If names are not given, the function just reads all data in folder
    else:
        df_names = []
        path, dirs, files = next(os.walk(filepath))
        file_count = len(files)
        for i in range(file_count):
            temp_df = pd.read_excel(filepath + files[i])
            df_list.append(temp_df)
            df_names.append(files[i][:-5])

    framemap = FrameMap(df_list, df_names)

    # return memory optimized version if selected
    if optimize:
        framemap = framemap.optimize()

    return framemap


def readm_pickle(filepath: str, df_names: List[str] = None, optimize: bool = False) -> FrameMap:
    """
    Reads multiple files in a directory, returns a FrameMap
    If df_names == None, it iterates the whole directory.
    If optimize == True, returns a memory optimized version

    Receives the path and optionally a list of the dataframes names.

    Returns a FrameMap

    the folder should have only pkl files, no .txt

    Parameters
    ----------
    filepath : str
        the path of the folder to be read
    df_names : List[str], default None
        a list with the names of the files
    optimize : bool, default False
        if True, returns memory optimized version of dataframes

    Returns
    -------
    FrameMap
    """
    df_list = []

    # Here the function uses the names of the dataframes to read the files
    if df_names is not None:
        df_names = np.char.array(df_names)
        filepath = np.full(df_names.shape, filepath)
        reader = filepath + df_names + '.pkl'

        df_list = [pd.read_pickle(i) for i in reader]

    # If names are not given, the function just reads all data in folder
    else:
        df_names = []
        path, dirs, files = next(os.walk(filepath))
        file_count = len(files)
        for i in range(file_count):
            temp_df = pd.read_pickle(filepath + files[i])
            df_list.append(temp_df)
            df_names.append(files[i][:-4])

    framemap = FrameMap(df_list, df_names)

    # return memory optimized version if selected
    if optimize:
        framemap = framemap.optimize()

    return framemap


def readm_parquet(filepath: str, df_names: List[str] = None, optimize: bool = False) -> FrameMap:
    """
    Reads multiple files in a directory, returns a FrameMap
    If df_names == None, it iterates the whole directory.
    If optimize == True, returns a memory optimized version

    Receives the path and optionally a list of the dataframes names.

    Returns a FrameMap

    the folder should have only parquet files, no .txt

    Parameters
    ----------
    filepath : str
        the path of the folder to be read
    df_names : List[str], default None
        a list with the names of the files
    optimize : bool, default False
        if True, returns memory optimized version of dataframes

    Returns
    -------
    FrameMap
    """
    df_list = []

    # Here the function uses the names of the dataframes to read the files
    if df_names is not None:
        df_names = np.char.array(df_names)
        filepath = np.full(df_names.shape, filepath)
        reader = filepath + df_names + '.parquet'

        df_list = [pd.read_parquet(i) for i in reader]

    # If names are not given, the function just reads all data in folder
    else:
        df_names = []
        path, dirs, files = next(os.walk(filepath))
        file_count = len(files)
        for i in range(file_count):
            temp_df = pd.read_parquet(filepath + files[i])
            df_list.append(temp_df)
            df_names.append(files[i][:-8])

    framemap = FrameMap(df_list, df_names)

    # return memory optimized version if selected
    if optimize:
        framemap = framemap.optimize()

    return framemap
