# Retail Sales Data Engineering Project

## End-to-End Architecture

```mermaid
flowchart LR
    A["Retail CSV Datasets"]
    B["Azure Data Factory"]
    C["ADLS Gen2 - Bronze"]
    D["Azure Databricks - PySpark"]
    E["ADLS Gen2 - Silver"]
    F["ADLS Gen2 - Gold"]
    G["Databricks SQL"]
    H["Databricks AI/BI Dashboard"]

    A --> B --> C
    C --> D
    D --> E
    E --> D
    D --> F --> G --> H
```

## Technology Stack

- Azure Data Factory
- Azure Data Lake Storage Gen2
- Azure Databricks
- PySpark
- Delta Lake
- Databricks SQL
- Databricks AI/BI Dashboard

## Architecture Pattern

Medallion Architecture: Bronze → Silver → Gold.
