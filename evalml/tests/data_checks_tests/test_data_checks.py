import numpy as np
import pandas as pd

from evalml.data_checks.data_check import DataCheck
from evalml.data_checks.data_check_message import (
    DataCheckError,
    DataCheckWarning
)
from evalml.data_checks.data_checks import DataChecks
from evalml.data_checks.default_data_checks import DefaultDataChecks
from evalml.data_checks.utils import EmptyDataChecks


def test_data_checks(X_y):
    X, y = X_y

    class MockDataCheck(DataCheck):
        def validate(self, X, y):
            return []

    class MockDataCheckWarning(DataCheck):
        def validate(self, X, y):
            return [DataCheckWarning("warning one", self.name)]

    class MockDataCheckError(DataCheck):
        def validate(self, X, y):
            return [DataCheckError("error one", self.name)]

    class MockDataCheckErrorAndWarning(DataCheck):
        def validate(self, X, y):
            return [DataCheckError("error two", self.name), DataCheckWarning("warning two", self.name)]

    data_checks_list = [MockDataCheck(), MockDataCheckWarning(), MockDataCheckError(), MockDataCheckErrorAndWarning()]
    data_checks = DataChecks(data_checks=data_checks_list)
    assert data_checks.validate(X, y) == [DataCheckWarning("warning one", "MockDataCheckWarning"),
                                          DataCheckError("error one", "MockDataCheckError"),
                                          DataCheckError("error two", "MockDataCheckErrorAndWarning"),
                                          DataCheckWarning("warning two", "MockDataCheckErrorAndWarning")]


def test_empty_data_checks(X_y):
    X, y = X_y
    data_checks = EmptyDataChecks()
    assert data_checks.validate(X, y) == []


def test_default_data_checks_classification(X_y):
    X = pd.DataFrame({'lots_of_null': [None, None, None, None, "some data"],
                      'all_null': [None, None, None, None, None],
                      'also_all_null': [None, None, None, None, None],
                      'no_null': [1, 2, 3, 4, 5],
                      'id': [0, 1, 2, 3, 4],
                      'has_label_leakage': [100, 200, 100, 200, 100]})
    y = pd.Series([0, 1, np.nan, 1, 0])
    data_checks = DefaultDataChecks()
    assert data_checks.validate(X, y) == [DataCheckWarning("Column 'all_null' is 95.0% or more null", "HighlyNullDataCheck"),
                                          DataCheckWarning("Column 'also_all_null' is 95.0% or more null", "HighlyNullDataCheck"),
                                          DataCheckWarning("Column 'id' is 100.0% or more likely to be an ID column", "IDColumnsDataCheck"),
                                          DataCheckWarning("Column 'has_label_leakage' is 95.0% or more correlated with the target", "LabelLeakageDataCheck"),
                                          DataCheckError("1 row(s) (20.0%) of target values are null", "InvalidTargetDataCheck")]

    # multiclass
    y = pd.Series([0, 1, np.nan, 2, 0])
    data_checks = DefaultDataChecks()
    assert data_checks.validate(X, y) == [DataCheckWarning("Column 'all_null' is 95.0% or more null", "HighlyNullDataCheck"),
                                          DataCheckWarning("Column 'also_all_null' is 95.0% or more null", "HighlyNullDataCheck"),
                                          DataCheckWarning("Column 'id' is 100.0% or more likely to be an ID column", "IDColumnsDataCheck"),
                                          DataCheckError("1 row(s) (20.0%) of target values are null", "InvalidTargetDataCheck")]


def test_default_data_checks_regression(X_y):
    X = pd.DataFrame({'lots_of_null': [None, None, None, None, "some data"],
                      'all_null': [None, None, None, None, None],
                      'also_all_null': [None, None, None, None, None],
                      'no_null': [1, 2, 3, 4, 5],
                      'id': [0, 1, 2, 3, 4],
                      'has_label_leakage': [100, 200, 100, 200, 100]})
    y = pd.Series([0.3, 100.0, np.nan, 1.0, 0.2])
    data_checks = DefaultDataChecks()
    assert data_checks.validate(X, y) == [DataCheckWarning("Column 'all_null' is 95.0% or more null", "HighlyNullDataCheck"),
                                          DataCheckWarning("Column 'also_all_null' is 95.0% or more null", "HighlyNullDataCheck"),
                                          DataCheckWarning("Column 'id' is 100.0% or more likely to be an ID column", "IDColumnsDataCheck"),
                                          DataCheckError("1 row(s) (20.0%) of target values are null", "InvalidTargetDataCheck")]