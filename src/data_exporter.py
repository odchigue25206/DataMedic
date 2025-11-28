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

    # Dunder method
    def __repr__(self):
        return f"<DataExporter columns={self._data.shape[1]}>"
