class DataPipeline:
    """Chains cleaning, visualization, and export steps."""

    def __init__(self, doctor, visualizer=None, exporter=None, reporter=None):
        self.doctor = doctor
        self.visualizer = visualizer
        self.exporter = exporter
        self.reporter = reporter

    def run(self):
        print("=== Diagnosing Issues ===")
        for s in self.doctor.diagnose():
            print("-", s)

        print("\n=== Applying Treatments ===")
        self.doctor.treat()
        print("\n=== Fix Log ===")
        for log in self.doctor.get_fix_log():
            print("-", log)

        if self.visualizer:
            print("\n=== Visualizing ===")
            self.visualizer.plot_missing()
            self.visualizer.plot_outliers()

        if self.exporter:
            print("\n=== Exporting Cleaned Data ===")
            self.exporter.to_csv()
            self.exporter.to_excel()
            self.exporter.to_json()

        if self.reporter:
            self.reporter.report()
            self.reporter.export_report()
            print("\n=== Report Generated ===")

    # Dunder method
    def __repr__(self):
        return f"<DataPipeline doctor={self.doctor}, visualizer={self.visualizer}, exporter={self.exporter}>"
