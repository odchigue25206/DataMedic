import pandas as pd

class DataExporter:
    """Exports cleaned datasets in CSV, Excel, JSON formats."""

    def __init__(self, dataframe):
        self._data = dataframe

    def to_csv(self, file_name="cleaned_data.csv"):
        self._data.to_csv(file_name, index=False)

    def to_excel(self, file_name="cleaned_data.xlsx"):
        self._data.to_excel(file_name, index=False)

    def to_json(self, file_name="cleaned_data.json"):
        self._data.to_json(file_name, orient="records")

    def __repr__(self):
        return f"<DataExporter columns={self._data.shape[1]}>"

class ReportGenerator:
    def __init__(self, dataframe):
        self._data = dataframe
        self._report_data = {}
        self._score = 0

    def report(self):
        missing = self._data.isnull().sum().to_dict()
        duplicates = self._data.duplicated().sum()
        outliers = {}
        for col in self._data.select_dtypes(include='number').columns:
            mean = self._data[col].mean()
            std = self._data[col].std()
            outliers[col] = ((self._data[col] < mean - 3*std) | (self._data[col] > mean + 3*std)).sum()

        self._report_data = {
            "missing": missing,
            "duplicates": duplicates,
            "outliers": outliers
        }
        return self._report_data

    def health_score(self):
        if not self._report_data:
            self.report()
        total = sum(self._report_data["missing"].values()) + \
                self._report_data["duplicates"] + \
                sum(self._report_data["outliers"].values())
        self._score = max(0, 100 - total)
        return self._score

    def export_report(self, file_name="report.txt"):
        if not self._report_data:
            self.report()
        with open(file_name, "w") as f:
            f.write(str(self._report_data))

    def __repr__(self):
        return "<ReportGenerator>"

class DataOutput:
    def __init__(self, dataframe):
        self.exporter = DataExporter(dataframe)
        self.reporter = ReportGenerator(dataframe)

    def export_all(self):
        self.exporter.to_csv()
        self.exporter.to_excel()
        self.exporter.to_json()

    def generate_report(self):
        self.reporter.report()
        self.reporter.export_report()

    def full_output(self):
        self.export_all()
        self.generate_report()
        return {
            "report": self.reporter._report_data,
            "health_score": self.reporter.health_score()
        }

    def __repr__(self):
        return "<DataOutput>"
  
