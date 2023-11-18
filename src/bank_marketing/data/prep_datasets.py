"""This module includes the functions to prepare datasets for ML applications.
"""

from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


@dataclass
class Dataset:
    """A dataclass used to represent a Dataset

    Attributes
    ----------
    train_x : Pandas DataFrame
        the dataframe of input features w.r.t training split
    val_x : Pandas DataFrame
        the dataframe of input features w.r.t validation split
    test_x : Pandas DataFrame
        the dataframe of input features w.r.t testing split
    train_y : Pandas Series
        the series of output label w.r.t training split
    val_y : Pandas Series
        tthe series of output label w.r.t validation split
    test_y : Pandas Series
        the series of output label w.r.t testing split
    """

    train_x: pd.DataFrame
    val_x: pd.DataFrame
    test_x: pd.DataFrame
    train_y: pd.Series
    val_y: pd.Series
    test_y: pd.Series


def prepare_binary_classfication_tabular_data(
    data_frame: pd.DataFrame,
    predictors: List[str],
    predicted: str,
    pos_neg_pair: Tuple[str, str] | None = None,
    splits_sizes: Tuple[float] = (0.7, 0.1, 0.2),
    seed: int = 42,
) -> Dataset:
    """Prepare the training/validation/test inputs (X) and outputs (y) for binary clasification modeling

    Args:
    ----
        data_frame (pd.DataFrame): aggregated data frame
        predictors (List[str]): list of predictors column names
        predicted (str): column name of the predicted outcome
        pos_neg_pair (Tuple[str,str], optional): groundtruth positive/negative labels. Defaults to None.
        splits_sizes (List[float], optional): list of relative size portions for training, validation, test data, respectively. Defaults to [0.7,0.1,0.2].
        seed (int, optional): random seed. Defaults to 42.

    Returns:
    -------
        Dataset: datassets for binary classification with training/validation/test splits
    """
    X = data_frame[predictors].copy()  # noqa
    y = data_frame[predicted].copy()
    if pos_neg_pair:
        postive, negative = pos_neg_pair
        y = y.replace({postive: 1, negative: 0})
    train_size, valid_size, test_size = splits_sizes
    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=test_size, random_state=seed)
    valid_size /= train_size + valid_size
    train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=valid_size, random_state=seed)
    dataset = Dataset(train_x, val_x, test_x, train_y, val_y, test_y)
    return dataset
