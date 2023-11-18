import logging
import pytest
import numpy as np
from bank_marketing.data.prep_datasets import prepare_binary_classfication_tabular_data

def test_prepare_binary_classfication_tabular_data_X_y_equal_splits(dataframe, predictors, predicted):
    '''
	test the equality of X and y for the three generated splits.
    > This example is provided to you in order to assist with the following test functions
	'''
    dataset = prepare_binary_classfication_tabular_data(dataframe, 
                                                        predictors, 
                                                        predicted, 
                                                        pos_neg_pair=('yes', 'no'))
    logging.info("prepare_binary_classification_tabular_data was called successfully without errors.")
    for_train = len(dataset.train_x) == len(dataset.train_y)
    if not for_train:
        logging.error("The sizes of feature (X) and label (y) data for the training split are not equal.")
    for_val = len(dataset.val_x) == len(dataset.val_y)
    if not for_val:
        logging.error("The sizes of feature (X) and label (y) data for the validation split are not equal.")
    for_test = len(dataset.test_x) == len(dataset.test_y)
    if not for_test:
        logging.error("The sizes of feature (X) and label (y) data for the testing split are not equal.")
    assert for_train and for_val and for_test
    
def test_prepare_binary_classfication_tabular_data_correctness(dataframe, predictors, predicted):
    '''
	test the splits correctness in regards to X and y alignment 
    i.e., check if each x is associated with its correct y.
	'''
    dataframe['gen_id'] = dataframe.index
    response_dict = {gen_id:response 
                     for gen_id, response in zip(dataframe['gen_id'], dataframe['curr_outcome'])}
    dataset = prepare_binary_classfication_tabular_data(dataframe, 
                                                        predictors + ['gen_id'], 
                                                        predicted, 
                                                        None)
    logging.info("prepare_binary_classification_tabular_data was called successfully without errors.")
    train_y_true = dataset.train_x.apply(lambda row:response_dict[row['gen_id']], axis=1)
    val_y_true = dataset.val_x.apply(lambda row:response_dict[row['gen_id']], axis=1)
    test_y_true = dataset.test_x.apply(lambda row:response_dict[row['gen_id']], axis=1) 
    train_is_aligned = (train_y_true == dataset.train_y).all()
    if not train_is_aligned:
        logging.error("The features (X) and labels (y) for the training split are aligned.")
    val_is_aligned = (val_y_true == dataset.val_y).all()
    if not val_is_aligned:
        logging.error("The features (X) and labels (y) for the validation split are aligned.")
    test_is_aligned = (test_y_true == dataset.test_y).all()
    if not test_is_aligned:
        logging.error("The features (X) and labels (y) for the testing split are aligned.")
    assert train_is_aligned and val_is_aligned and test_is_aligned
     
@pytest.mark.parametrize("splits_sizes", [
    (0.7, 0.2, 0.1),
    (0.7, 0.1, 0.2),
    (0.2, 0.4, 0.4),
])
def test_prepare_binary_classfication_tabular_data_splits_sizes(splits_sizes, dataframe, predictors, predicted):
    '''
	test the actual splits sizes are conform to the provided ratios.
	'''
    total_rows = len(dataframe)
    expected_absolute_sizes = np.round(total_rows * np.array(splits_sizes))
    dataset = prepare_binary_classfication_tabular_data(dataframe, 
                                                        predictors, 
                                                        predicted, 
                                                        splits_sizes=splits_sizes,
                                                        seed = 42)
    logging.info("prepare_binary_classification_tabular_data was called successfully without errors.")
    train_diff = abs(expected_absolute_sizes[0] - len(dataset.train_x))
    if train_diff > 1:
        logging.error("The actual size of the training split is not as expected.")
    val_diff = abs(expected_absolute_sizes[1] - len(dataset.val_x))
    if val_diff > 1:
        logging.error("The actual size of the validation split is not as expected.")
    test_diff = abs(expected_absolute_sizes[2] - len(dataset.test_x))
    if test_diff > 1:
        logging.error("The actual size of the testing split is not as expected.")
    assert train_diff <= 1 and val_diff <= 1 and test_diff <= 1

@pytest.mark.parametrize("seed, row", [
    (43, 0),
    (77, 10),
    (89, 50)
])
def test_prepare_binary_classfication_tabular_data_reproducibility(seed, row, dataframe, predictors, predicted):
    '''
	test the generated splits with fixed seed are the same based on 
    an arbitrary row index (argument).
	'''
    dataset_1 = prepare_binary_classfication_tabular_data(dataframe, 
                                                        predictors, 
                                                        predicted, 
                                                        seed = seed)
    dataset_2 = prepare_binary_classfication_tabular_data(dataframe, 
                                                        predictors, 
                                                        predicted, 
                                                        seed = seed)
    logging.info("prepare_binary_classification_tabular_data was called successfully without errors.")
    train_x_eq = (dataset_1.train_x.iloc[row] == dataset_2.train_x.iloc[row]).all()
    if not train_x_eq:
        logging.error("The training split is not the same with fixed seed.")
    val_x_eq = (dataset_1.val_x.iloc[row] == dataset_2.val_x.iloc[row]).all()
    if not val_x_eq:
        logging.error("The validation split is not the same with fixed seed.")
    test_x_eq = (dataset_1.test_x.iloc[row] == dataset_2.test_x.iloc[row]).all()
    if not test_x_eq:
        logging.error("The testing split is not the same with fixed seed.")
    assert train_x_eq and val_x_eq and test_x_eq

@pytest.mark.parametrize("seed_1, seed_2, row", [
    (42, 43, 0),
    (51, 63, 10)
])
def test_prepare_binary_classfication_tabular_data_variability(seed_1, seed_2, row, dataframe, predictors, predicted):
    '''
	test the generated splits with different seeds are actually different based on 
    an arbitrary row index (argument).
	'''
    dataset_1 = prepare_binary_classfication_tabular_data(dataframe, 
                                                        predictors, 
                                                        predicted, 
                                                        seed = seed_1)
    dataset_2 = prepare_binary_classfication_tabular_data(dataframe, 
                                                        predictors, 
                                                        predicted, 
                                                        seed = seed_2)
    logging.info("prepare_binary_classification_tabular_data was called successfully without errors.")
    train_x_neq = (dataset_1.train_x.iloc[row] != dataset_2.train_x.iloc[row]).any()
    if not train_x_neq:
        logging.error("The training split is not different when seed is changed.")
    val_x_neq = (dataset_1.val_x.iloc[row] != dataset_2.val_x.iloc[row]).any()
    if not val_x_neq:
        logging.error("The validation split is not different when seed is changed.")
    test_x_neq = (dataset_1.test_x.iloc[row] != dataset_2.test_x.iloc[row]).any()
    if not test_x_neq:
        logging.error("The testing split is not different when seed is changed.")
    assert train_x_neq and val_x_neq and test_x_neq
