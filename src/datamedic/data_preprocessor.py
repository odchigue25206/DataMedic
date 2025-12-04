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
    def __init__(self, dataframe):
        super().__init__(dataframe)
        self._fix_log = []

    def diagnose(self):
        issues = self.inspect()
        suggestions = {}

        missing = issues['missing']
        for col, count in missing.items():
            if count > 0:
                suggestions[col] = suggestions.get(col, []) + [f"{count} missing values"]

        if issues['duplicates'] > 0:
            suggestions["Dataset"] = suggestions.get("Dataset", []) + [f"{issues['duplicates']} duplicate rows"]

        outliers = issues['outliers']
        for col, count in outliers.items():
            if count > 0:
                suggestions[col] = suggestions.get(col, []) + [f"{count} outliers detected"]

        return suggestions

    def treat(self, treat_missing=True, treat_duplicates=True, treat_outliers=True):
        if treat_missing:
            self.fix_missing()
        if treat_duplicates:
            self.fix_duplicates()
        if treat_outliers:
            self.fix_outliers()
        return self._data

    def fix_missing(self):
        for col in self._data.columns:
            if self._data[col].isnull().sum() == 0:
                continue

            if pd.api.types.is_numeric_dtype(self._data[col]):
                mean_val = self._data[col].mean()
                fill_value = int(round(mean_val)) if pd.api.types.is_integer_dtype(self._data[col]) else mean_val
            else:
                mode_val = self._data[col].mode()
                fill_value = mode_val[0] if not mode_val.empty else "Unknown"

            self._data[col] = self._data[col].fillna(fill_value)
            self._fix_log.append(f"Filled missing values in '{col}' with {fill_value}.")

    def fix_duplicates(self):
        before = self._data.shape[0]
        self._data.drop_duplicates(inplace=True)
        removed = before - self._data.shape[0]
        self._fix_log.append(f"Removed {removed} duplicate rows.")

    def fix_outliers(self):
        numeric_cols = self._data.select_dtypes(include="number").columns
        for col in numeric_cols:
            Q1 = self._data[col].quantile(0.25)
            Q3 = self._data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            self._data[col] = self._data[col].clip(lower=lower, upper=upper)
            self._fix_log.append(f"Handled outliers in '{col}' using 1.5*IQR clipping.")

    def get_fix_log(self):
        return self._fix_log

    def __repr__(self):
        return f"<DataCleaner rows={self._data.shape[0]}, fixes={len(self._fix_log)}>"

    def __lt__(self, other):
        if not isinstance(other, DataCleaner):
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
