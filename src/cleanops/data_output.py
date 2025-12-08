import pandas as pd
import json
from typing import Dict, Any


class DataExporter:
    """Export DataFrame in CSV, Excel, or JSON formats."""

    def __init__(self, dataframe: pd.DataFrame) -> None:
        self._data = dataframe.copy()

    def to_csv(self, file_name: str = "cleaned_data.csv") -> None:
        self._data.to_csv(file_name, index=False)

    def to_excel(self, file_name: str = "cleaned_data.xlsx") -> None:
        self._data.to_excel(file_name, index=False)

    def to_json(self, file_name: str = "cleaned_data.json") -> None:
        self._data.to_json(file_name, orient="records", indent=4)

    def __repr__(self) -> str:
        return f"<DataExporter columns={self._data.shape[1]}>"


class ReportGenerator:
    """Create a summary report of dataset issues such as missing values, duplicates, and outliers."""

    def __init__(self, dataframe: pd.DataFrame) -> None:
        self._data = dataframe.copy()
        self._report_data: Dict[str, Any] = {}
        self._score: int = 0

    def report(self) -> Dict[str, Any]:
        missing = self._data.isnull().sum().to_dict()
        duplicates = self._data.duplicated().sum()
        outliers: Dict[str, int] = {}
        for col in self._data.select_dtypes(include="number").columns:
            mean = self._data[col].mean()
            std = self._data[col].std()
            outliers[col] = int(((self._data[col] < mean - 3*std) | (self._data[col] > mean + 3*std)).sum())

        self._report_data = {"missing": missing, "duplicates": duplicates, "outliers": outliers}
        return self._report_data

    def export_report(self, file_name: str = "report.txt") -> None:
        """Export the data report to a TXT file."""
        if not self._report_data:
            self.report()

        with open(file_name, "w") as f:
            for key, value in self._report_data.items():
                f.write(f"{key.upper()}:\n{value}\n\n")

    def __repr__(self) -> str:
        return "<ReportGenerator>"



class DataOutput:
    """Combine exporting and reporting in one call."""

    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.exporter = DataExporter(dataframe)
        self.reporter = ReportGenerator(dataframe)

    def export_all(self) -> None:
        self.exporter.to_csv()
        self.exporter.to_excel()
        self.exporter.to_json()

    def generate_report(self) -> None:
        self.reporter.report()
        self.reporter.export_report()

    def full_output(self) -> Dict[str, Any]:
        self.export_all()
        self.generate_report()
        return {
            "report": self.reporter._report_data
        }

    def __repr__(self) -> str:
        return "<DataOutput>"
