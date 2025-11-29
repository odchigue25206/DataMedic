import pandas as pd

class DataOrganizer:
    """
    Sorts DataFrame columns or rows alphabetically and exports output.
    """

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
        """Return number of rows for len() function."""
        return len(self._data)

    def __eq__(self, other):
        """Compare two DataOrganizer objects by their DataFrame content."""
        if not isinstance(other, DataOrganizer):
            return NotImplemented
        return self._data.equals(other._data)
