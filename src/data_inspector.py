import pandas as pd

class DataInspector:
    """Scans a dataset and identifies common data quality issues."""

    def __init__(self, dataframe: pd.DataFrame):
        self._data = dataframe  # protected attribute
        self._issues = {}

    def inspect(self):
        self._issues['missing'] = self.detect_missing()
        self._issues['duplicates'] = self.detect_duplicates()
        self._issues['outliers'] = self.detect_outliers()
        return self._issues

    def detect_missing(self):
        return self._data.isnull().sum()

    def detect_duplicates(self):
        return self._data.duplicated().sum()

    def detect_outliers(self):
        outliers = {}
        numeric_cols = self._data.select_dtypes(include="number").columns
        for col in numeric_cols:
            Q1 = self._data[col].quantile(0.25)
            Q3 = self._data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            count = self._data[(self._data[col] < lower) | (self._data[col] > upper)].shape[0]
            outliers[col] = count
        return outliers

    def get_summary(self):
        return self._issues

    # Dunder methods
    def __repr__(self):
        return f"<DataInspector rows={self._data.shape[0]}, cols={self._data.shape[1]}>"

    def __eq__(self, other):
        if not isinstance(other, DataInspector):
            return False
        return self._data.equals(other._data)
