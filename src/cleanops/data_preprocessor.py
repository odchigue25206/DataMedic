import pandas as pd
from typing import Dict, Any


class DataInspector:
    """Scan dataset and identify common data quality issues."""

    def __init__(self, dataframe: pd.DataFrame) -> None:
        self._data = dataframe.copy()
        self._issues: Dict[str, Any] = {}

    def inspect(self) -> Dict[str, Any]:
        """Run all inspections and return issues."""
        self._issues['missing'] = self.detect_missing()
        self._issues['duplicates'] = self.detect_duplicates()
        self._issues['outliers'] = self.detect_outliers()
        return self._issues

    def detect_missing(self) -> pd.Series:
        return self._data.isnull().sum()

    def detect_duplicates(self) -> int:
        return self._data.duplicated().sum()

    def detect_outliers(self) -> Dict[str, int]:
        outliers: Dict[str, int] = {}
        numeric_cols = self._data.select_dtypes(include="number").columns
        for col in numeric_cols:
            Q1, Q3 = self._data[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
            count = ((self._data[col] < lower) | (self._data[col] > upper)).sum()
            outliers[col] = int(count)
        return outliers

    def get_summary(self) -> Dict[str, Any]:
        return self._issues

    def __repr__(self) -> str:
        return f"<DataInspector rows={self._data.shape[0]}, cols={self._data.shape[1]}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DataInspector) and self._data.equals(other._data)


class DataCleaner(DataInspector):
    """Clean data: handle missing values, duplicates, and outliers."""

    def __init__(self, dataframe: pd.DataFrame) -> None:
        super().__init__(dataframe)
        self._fix_log: list[str] = []

    def diagnose(self) -> Dict[str, list[str]]:
        """Return a dictionary of issues and suggested fixes."""
        issues = self.inspect()
        suggestions: Dict[str, list[str]] = {}

        for col, count in issues['missing'].items():
            if count > 0:
                suggestions[col] = [f"{count} missing values"]

        if issues['duplicates'] > 0:
            suggestions["Dataset"] = [f"{issues['duplicates']} duplicate rows"]

        for col, count in issues['outliers'].items():
            if count > 0:
                suggestions[col] = suggestions.get(col, []) + [f"{count} outliers detected"]

        return suggestions

    def treat(
        self,
        treat_missing: bool = True,
        treat_duplicates: bool = True,
        treat_outliers: bool = True,
        missing_strategy: str = "mean",
        outlier_strategy: str = "clip",
    ) -> pd.DataFrame:
        """Apply cleaning strategies to the data."""
        if treat_missing:
            self.fix_missing(strategy=missing_strategy)
        if treat_duplicates:
            self.fix_duplicates()
        if treat_outliers:
            self.fix_outliers(strategy=outlier_strategy)
        return self._data

    def fix_missing(self, strategy: str = "mean") -> None:
        """Fill missing values using a strategy: mean, median, or mode."""
        for col in self._data.columns:
            if self._data[col].isnull().sum() == 0:
                continue

            if pd.api.types.is_numeric_dtype(self._data[col]):
                if strategy == "mean":
                    fill_value = self._data[col].mean()
                elif strategy == "median":
                    fill_value = self._data[col].median()
                else:
                    raise ValueError("strategy must be 'mean' or 'median'")
            else:
                mode_val = self._data[col].mode()
                fill_value = mode_val[0] if not mode_val.empty else "Unknown"

            self._data[col] = self._data[col].fillna(fill_value)
            self._fix_log.append(f"Filled missing '{col}' with {fill_value}")

    def fix_duplicates(self, column: str) -> None:
        before = self._data.shape[0]
        self._data.drop_duplicates(subset=[column], inplace=True)
        removed = before - self._data.shape[0]
        self._fix_log.append(
            f"Removed {removed} duplicate rows based on column '{column}'"
        )

    def fix_outliers(self, strategy: str = "clip") -> None:
        """Handle outliers using strategy. Currently only 'clip' is supported."""
        numeric_cols = self._data.select_dtypes(include="number").columns
        for col in numeric_cols:
            Q1, Q3 = self._data[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
            if strategy == "clip":
                self._data[col] = self._data[col].clip(lower=lower, upper=upper)
                self._fix_log.append(f"Clipped outliers in '{col}'")
            else:
                raise ValueError("strategy must be 'clip' for now")

    def get_fix_log(self) -> list[str]:
        return self._fix_log

    def __repr__(self) -> str:
        return f"<DataCleaner rows={self._data.shape[0]}, fixes={len(self._fix_log)}>"

    
class DataOrganizer:
    """Sort DataFrame columns or rows alphabetically."""

    def __init__(self, dataframe: pd.DataFrame):
        self._data = dataframe.copy()

    def sort_columns(self) -> pd.DataFrame:
        """Sort columns alphabetically."""
        self._data = self._data[sorted(self._data.columns)]
        return self._data

    def sort_rows(self, column_name: str) -> pd.DataFrame:
        """Sort rows alphabetically using a specific column."""
        if column_name not in self._data.columns:
            raise ValueError(f"Column '{column_name}' does not exist.")
        self._data = self._data.sort_values(by=column_name)
        return self._data

    def __repr__(self) -> str:
        return f"<DataOrganizer rows={len(self._data)}, columns={len(self._data.columns)}>"

    def __len__(self) -> int:
        return len(self._data)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DataOrganizer) and self._data.equals(other._data)
