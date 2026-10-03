# delta_vs_parquet
Small code to check Delta tables vs Parquet behaviour.

## 1. Virtual env and libraries

Some steps are missing because I assume that, if you are here you know what you are doing.

```python
python -m venv .venv

python -m pip install deltalake pyarrow
```

## 2. Create the code to check Delta vs. Parquet

Check the file `check_delta.py` (table saved as Arrow).
Or use `check_delta_pandas.py` where table is saved as delta and read with pandas for the parquet case.

## 3. Run it

```python
python check_delta.py
```

## 4. Interpretation

As expected with Parquet you are reading every data, not the LAST data ingested.


