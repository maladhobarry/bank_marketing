import pytest
from bank_marketing.data.make_datasets import make_bank_marketing_dataframe

def pytest_addoption(parser):
    parser.addoption("--db", action="store")
    parser.addoption("--sed", action="store")


@pytest.fixture(scope='module')
def dataframe(request):
    df = make_bank_marketing_dataframe(
                request.config.option.db,
                request.config.option.sed)
    return df

@pytest.fixture(scope='module')
def predictors():
    predictors = ['age',
                'job',
                'marital',
                'education',
                'comm_month',
                'comm_day',
                'comm_type',
                'curr_n_contact',
                'days_since_last_campaign',
                'last_n_contact',
                'last_outcome',
                'emp.var.rate',
                'cons.price.idx',
                'cons.conf.idx',
                'euribor3m',
                'nr.employed',
                'housing',
                'loan',
                'default']
    return predictors

@pytest.fixture(scope='module')
def predicted():
    return 'curr_outcome'

