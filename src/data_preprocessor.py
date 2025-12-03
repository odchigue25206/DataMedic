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

    def __repr__(self):
        return f"<DataInspector rows={self._data.shape[0]}, cols={self._data.shape[1]}>"

    def __eq__(self, other):
        if not isinstance(other, DataInspector):
            return False
        return self._data.equals(other._data)


class DataCleaner(DataInspector):
    """Extends DataInspector with diagnosis and treatment capabilities."""

    def __init__(self, dataframe):
        super().__init__(dataframe)
        self._fix_log = []

    def diagnose(self):
        issues = self.inspect()
        suggestions = []

        if issues['missing'].sum() > 0:
            suggestions.append("Missing values detected. Consider filling or removing them.")
        if issues['duplicates'] > 0:
            suggestions.append("Duplicate rows found. You may remove duplicates.")
        if sum(issues['outliers'].values()) > 0:
            suggestions.append("Outliers detected in numeric columns.")

        return suggestions

    def treat(self):
        self.fix_missing()
        self.fix_duplicates()
        self.fix_outliers()
        return self._data

    def fix_missing(self):
        self._data.fillna(self._data.mean(numeric_only=True), inplace=True)
        self._fix_log.append("Missing values filled.")

    def fix_duplicates(self):
        before = self._data.shape[0]
        self._data.drop_duplicates(inplace=True)
        after = self._data.shape[0]
        removed = before - after
        self._fix_log.append(f"{removed} duplicate rows removed.")

    def fix_outliers(self):
        numeric_cols = self._data.select_dtypes(include="number").columns
        for col in numeric_cols:
            self._data[col] = self._data[col].clip(
                lower=self._data[col].quantile(0.25),
                upper=self._data[col].quantile(0.75)
            )
        self._fix_log.append("Outliers handled.")

    def get_fix_log(self):
        return self._fix_log

    def __repr__(self):
        return f"<DataDoctor rows={self._data.shape[0]}, fixes={len(self._fix_log)}>"

    def __lt__(self, other):
        if not isinstance(other, DataDoctor):
            return NotImplemented
        return self._data.shape[0] < other._data.shape[0]


class DataOrganizer:
    """Sorts DataFrame columns or rows alphabetically."""

    def __init__(self, dataframe: pd.DataFrame):
        self._data = dataframe.copy()

    def sort_columns(self):
        """Sort columns alphabetically."""
        self._data = self._data[sorted(self._data.columns)]
        return self._data

    def sort_rows(self, column_name):
        """Sort rows alphabetically using a specific column."""
        if column_name not in self._data.columns:
            raise ValueError(f"Column '{column_name}' does not exist.")
        self._data = self._data.sort_values(by=column_name)
        return self._data

    def __repr__(self):
        return f"DataOrganizer(rows={len(self._data)}, columns={len(self._data.columns)})"

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        if not isinstance(other, DataOrganizer):
            return NotImplemented
        return self._data.equals(other._data)
