import pandas as pd
import pathlib

class DataGetter:
    """Fetch file data by name from a fixed base path."""

    def __init__(self, base_path=r"C:\Users\A S P I R E\OneDrive\Documents\Test"):
        self._base_path = pathlib.Path(base_path)  # protected attribute

    def read_file(self, file_name):
        try:
            return (self._base_path / file_name).read_text()
        except FileNotFoundError:
            return f"Error: '{file_name}' not found in '{self._base_path}'."
        except Exception as e:
            return f"Error: {e}"

    def read_csv(self, file_name):
        try:
            return pd.read_csv(self._base_path / file_name)
        except FileNotFoundError:
            print(f"Error: '{file_name}' not found.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def __repr__(self):
        return f"<DataGetter base_path='{self._base_path}'>"
