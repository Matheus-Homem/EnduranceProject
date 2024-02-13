# Directory Organization: *data*

The `data` directory contains **data inputs** needed for the correct execution.

It is structured as follows:

- `data/ingestion/` : Contains raw data files. *(mostly in .xlsx format)*
- `data/cleaned/` : Contains data files with renamed fields and correct data types. *(in .parquet format)*
- `data/refined/` : Contains refined data files ready for insights generation. *(in .parquet format)*