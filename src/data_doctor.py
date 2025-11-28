from data_inspector import DataInspector

class DataDoctor(DataInspector):
    """Extends DataInspector with diagnosis and treatment capabilities."""

    def __init__(self, dataframe):
        super().__init__(dataframe)
        self._fix_log = []  # protected attribute

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
            self._data[col] = self._data[col].clip(lower=self._data[col].quantile(0.25),
                                                   upper=self._data[col].quantile(0.75))
        self._fix_log.append("Outliers handled.")

    def get_fix_log(self):
        return self._fix_log

    # Dunder methods
    def __repr__(self):
        return f"<DataDoctor rows={self._data.shape[0]}, fixes={len(self._fix_log)}>"

    def __lt__(self, other):
        if not isinstance(other, DataDoctor):
            return NotImplemented
        return self._data.shape[0] < other._data.shape[0]
