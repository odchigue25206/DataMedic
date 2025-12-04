import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualizer:
    """Visualizes missing values and outliers."""

    def __init__(self, dataframe):
        self._data = dataframe  # protected

    def plot_missing(self):
        sns.heatmap(self._data.isnull(), cbar=False)
        plt.title("Missing Values Heatmap")
        plt.show()

    def plot_outliers(self):
        numeric_cols = self._data.select_dtypes(include="number").columns
        for col in numeric_cols:
            sns.boxplot(x=self._data[col])
            plt.title(f"Outliers in {col}")
            plt.show()

    # Dunder method
    def __repr__(self):
        return f"<DataVisualizer columns={self._data.shape[1]}>"
