from typing import Optional, Any

class DataPipeline:
    """Chain cleaning, visualization, and export steps."""

    def __init__(
        self,
        cleaner: Any,
        exporter: Optional[Any] = None,
        reporter: Optional[Any] = None,
    ):
        self.cleaner = cleaner
        self.exporter = exporter
        self.reporter = reporter

    def run(self) -> None:
        print("=== Diagnosing Issues ===")
        for col, msgs in self.cleaner.diagnose().items():
            for msg in msgs:
                print(f"- {col}: {msg}")

        print("\n=== Applying Treatments ===")
        self.cleaner.treat()
        print("\n=== Fix Log ===")
        for log in self.cleaner.get_fix_log():
            print("-", log)

        if self.exporter:
            print("\n=== Exporting Cleaned Data ===")
            self.exporter.to_csv()
            self.exporter.to_excel()
            self.exporter.to_json()

        if self.reporter:
            self.reporter.report()
            self.reporter.export_report()
            print("\n=== Report Generated ===")

    def __repr__(self) -> str:
        return f"<DataPipeline cleaner={self.cleaner}, exporter={self.exporter}>"
