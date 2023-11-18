"""This module includes the functions to train and evalure scikit-learn models
for bank marketing ML applications.
"""
import abc
from itertools import product
from typing import Dict, List

from bank_marketing.data.prep_datasets import Dataset
from bank_marketing.features.skl_build_features import AdvFeatureNames, make_advanced_data_transformer
from prettytable import PrettyTable
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline


def accuracy_evaluation(
    data_transfomer: Pipeline, classifier: abc.ABCMeta, data: Dataset, decimals: int = 3
) -> Dict[str, float]:
    """Compute binary classification accuracy scores on training/validation/testing data splits
       by a given pair of data transformer and classifier.

    Args:
    ----
        data_transfomer (Pipeline): sklearn feature engineering pipeline
        classifier (abc.ABCMeta): sklearn classifier class
        data (Dataset): datasets (training/validation/test)
        decimals (int, optional): number decimal digits of precision. Defaults to 3.

    Returns:
    -------
        Dict[str, float]: (keys: splits names, values: accuracy scores)
    """
    train_accuracy = accuracy_score(data.train_y.values, classifier.predict(data_transfomer.transform(data.train_x)))
    val_accuracy = accuracy_score(data.val_y.values, classifier.predict(data_transfomer.transform(data.val_x)))
    test_accuracy = accuracy_score(data.test_y.values, classifier.predict(data_transfomer.transform(data.test_x)))
    return {
        "train": round(train_accuracy, decimals),
        "val": round(val_accuracy, decimals),
        "test": round(test_accuracy, decimals),
    }


def train_and_evaluate(
    data: Dataset, data_transfomer: Pipeline, classifers_list: List[abc.ABCMeta]
) -> List[Dict[str, str | float]]:
    """Train each classifier of the list on the training data then evaluate it on all the splits

    Args:
    ----
        data (Dataset): datasets (training/validation/test)
        data_transfomer (Pipeline): sklearn feature engineering pipeline
        classifers_list (List[abc.ABCMeta]): list of sklearn classifier class

    Returns:
    -------
        List[Dict[str,str|float]]: A list of dictionaries, where each dictionary contains:
                                    'model': The name of the classifier class.
                                    Additional evaluation metrics (e.g., accuracy)
                                    obtained from the accuracy_evaluation function.
    """
    results = []
    for classifier in classifers_list:
        classifier_obj = classifier()
        classifier_obj.fit(data_transfomer.transform(data.train_x), data.train_y)
        results.append({"model": classifier.__name__, **accuracy_evaluation(data_transfomer, classifier_obj, data)})
    return results


def advanced_train_and_evaluate(
    data: Dataset,
    feature_names: AdvFeatureNames,
    clustering_algos_list: List[abc.ABCMeta],
    classifers_list: List[abc.ABCMeta],
) -> List[Dict[str, str | float]]:
    """Train each pair of clustering-based feature transformer and classifier of both lists
       on the training data then evaluate it on all the splits

    Args:
    ----
        data (Dataset): datasets (training/validation/test)
        feature_names (AdvFeatureNames): features names to be used for clustering and classification
        clustering_algos_list (List[abc.ABCMeta]): list of sklearn clustering algorithm class
        classifers_list (List[abc.ABCMeta]): list of sklearn classifier class

    Returns:
    -------
        List[Dict[str,str|float]]: accuracy scores w.r.t data splits for all
                                   the pairs of clustering algos and classfiers
    """
    results = []
    for clustering_algo, classifier in product(clustering_algos_list, classifers_list):
        classifier_obj = classifier()
        print(f"Running the pair of {clustering_algo.__name__} and {classifier.__name__}")
        data_transfomer = make_advanced_data_transformer(feature_names, clustering_algo)
        data_transfomer.fit(data.train_x)
        classifier_obj.fit(data_transfomer.transform(data.train_x), data.train_y)
        results.append(
            {
                "clustering_algo": clustering_algo.__name__,
                "classifier": classifier.__name__,
                **accuracy_evaluation(data_transfomer, classifier_obj, data),
            }
        )
    return results


def print_accuracy_results(results: List[Dict[str, str | float]] | Dict[str, str | float]) -> None:
    """Print the accuracy scoring results as pretty tables

    Args:
    ----
        results (List[Dict[str,str | float]] | Dict[str,str | float]): list of accuracy scores
    """
    tab = PrettyTable()
    if type(results) == dict:
        tab.field_names = list(results.keys())
        tab.add_row(list(results.values()))
    elif type(results) == list:
        tab.field_names = list(results[0].keys())
        tab.add_rows([list(result.values()) for result in results])
    print(tab)
