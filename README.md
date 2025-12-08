# CleanOps

A lightweight toolkit for inspecting, cleaning, organizing, and exporting datasets.  
Designed for quick data quality checks, automated cleaning, and report generation.

---

## 📌 Project Overview

CleanOps provides a simple workflow for handling messy datasets.  
It includes tools for:

- Detecting missing values  
- Identifying duplicate rows  
- Detecting outliers (IQR-based or statistical)  
- Cleaning + automatic fixing  
- Organizing dataset columns and rows  
- Exporting cleaned data (CSV / Excel / JSON)  
- Generating dataset health reports  
- Running complete pipelines combining cleaning, exporting, and reporting  

The goal is to make data preprocessing easier and more consistent.

---

## 📦 Installation

Install via pip:

```bash
pip install cleanops
```

Or, if you're installing from source:

```bash
pip install .
```

---

## 🚀 Example Usage

### **1. Inspecting and Cleaning a Dataset**

```python
import pandas as pd
from cleanops import DataCleaner

df = pd.read_csv("test_data_150.csv")

cleaner = DataCleaner(df)

# Diagnose issues
issues = cleaner.diagnose()
print("Issues found:", issues)

# Apply cleaning (missing, duplicates, outliers)
cleaned_df = cleaner.treat()

print(cleaned_df.head())
```

---

### **2. Exporting Cleaned Data**

```python
from cleanops import DataExporter

exporter = DataExporter(cleaned_df)

exporter.to_csv("output.csv")
exporter.to_excel("output.xlsx")
exporter.to_json("output.json")

```

---

### **3. Generating a Data Report**

```python
from cleanops import ReportGenerator

reporter = ReportGenerator(cleaned_df)
report = reporter.report()

print("Report:", report)

reporter.export_report("dataset_report.json")
```

---

### **4. Running a Full Data Pipeline**

```python
from cleanops import DataCleaner, DataOutput, DataPipeline
import pandas as pd

df = pd.read_csv("test_data_150.csv")

cleaner = DataCleaner(df)
output = DataOutput(df)

pipeline = DataPipeline(
    cleaner=cleaner, 
    exporter=output.exporter, 
    reporter=output.reporter
)
pipeline.run()
```

---

## 📄 License

This project is released under the MIT License.

---
