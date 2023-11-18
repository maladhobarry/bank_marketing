"""This module includes the functions and objects to build feature engineering pipelines
for bank marketing ML applications.
"""
import abc
from dataclasses import dataclass
from typing import List

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class HasBeenCalledBeforeTransformer(BaseEstimator, TransformerMixin):
    """A class used to perform has_been_called_before (new feature) derivation based
    on the value of days_since_last_campaign (existing feature)

    Methods
    -------
    fit()
        Do nothing
    transform(X)
        adds the new feature into the input data
    """

    def fit(self, X=None, y=None):  # noqa
        return self

    def transform(self, X, y=None):  # noqa
        X["has_been_called_before"] = (X.days_since_last_campaign != 999).astype(int)
        return X


@dataclass
class FeatureNames:
    """A dataclass used to represent Feature Names for a Basic ML Model

    Attributes
    ----------
    numerical : List[str]
        the list of numerical feature names
    categorical : List[str]
        the list of categorical feature names

    Methods
    -------
    features()
        Returns the list of all features
    """

    numerical: List[str]
    categorical: List[str]

    def features(self) -> List[str]:
        """Returns the list of all features

        Returns
        -------
            List[str]: list of all features
        """
        return self.numerical + self.categorical


def make_data_transformer(feature_names: FeatureNames) -> Pipeline:
    """Build the scikit-learn based basic data transformer

    Args:
    ----
        feature_names (FeatureNames): names of the numerical & categorical features

    Returns:
    -------
        Pipeline: the feature transformer pipeline
    """
    transformer_categorical = Pipeline(
        [
            ("onehot", OneHotEncoder(handle_unknown="error")),
        ]
    )
    transformer_numerical = Pipeline(
        [
            ("add_has_been_called_before", HasBeenCalledBeforeTransformer()),
            ("scale", StandardScaler()),
        ]
    )
    transformer = ColumnTransformer(
        [
            ("num", transformer_numerical, feature_names.numerical),
            ("cat", transformer_categorical, feature_names.categorical),
        ]
    )
    return transformer


@dataclass
class AdvFeatureNames:
    """A dataclass used to represent Feature Names for a Advanced ML Model

    Attributes
    ----------
    numerical_clustering : List[str]
        the list of numerical feature names for the clustering algorithm
    categorical_clustering : List[str]
        the list of categorical feature names for the clustering algorithm
    numerical_classifier : List[str]
        the list of numerical feature names for the classifier
    categorical_classifier : List[str]
        the list of categorical feature names for the classifier

    Methods
    -------
    clustering()
        Returns the list of all features for the clustering algorithm
    classifier()
        Returns the list of all features for the classifier
    """

    numerical_clustering: List[str]
    categorical_clustering: List[str]
    numerical_classifier: List[str]
    categorical_classifier: List[str]

    def clustering(self) -> List[str]:
        return self.numerical_clustering + self.categorical_clustering

    def classifier(self) -> List[str]:
        return self.numerical_classifier + self.categorical_classifier


def make_advanced_data_transformer(feature_names: AdvFeatureNames, clustering_algo: abc.ABCMeta) -> Pipeline:
    """Build the scikit-learn based advanced data transformer

    Args:
    ----
        feature_names (FeatureNames): names of the numerical & categorical features
                                      for both clustering & classifier algorithms involved

    Returns:
    -------
        Pipeline: the feature transformer pipeline
    """
    clustering_input_transformer = ColumnTransformer(
        [
            ("scaleCLS", StandardScaler(), feature_names.numerical_clustering),
            ("onehotCLS", OneHotEncoder(sparse_output=True), feature_names.categorical_clustering),
        ],
        remainder="drop",
    )
    clustering_pipeline = Pipeline(
        [
            ("dataCLS", clustering_input_transformer),
            ("algoCLS", clustering_algo()),
        ]
    )
    transformer_categorical = Pipeline(
        [
            ("onehot", OneHotEncoder(handle_unknown="error")),
        ]
    )
    transformer_numerical = Pipeline(
        [
            ("add_has_been_called_before", HasBeenCalledBeforeTransformer()),
            ("scale", StandardScaler()),
        ]
    )
    adv_data_transformer = ColumnTransformer(
        [
            ("clustering", clustering_pipeline, feature_names.clustering()),
            ("num", transformer_numerical, feature_names.numerical_classifier),
            ("cat", transformer_categorical, feature_names.categorical_classifier),
        ]
    )
    return adv_data_transformer
