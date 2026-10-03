from tempfile import TemporaryDirectory

import pandas as pd
import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

with TemporaryDirectory() as path:
    # Crear la tabla con datos e insertar otra vez.
    write_deltalake(path, pa.table({"id": [1, 2]}))
    write_deltalake(path, pa.table({"id": [3, 4]}), mode="append")

    # Borrar mediante Delta. Los archivos antiguos siguen en disco.
    DeltaTable(path).delete("id = 2")

    # Comparar las lecturas.
    delta = DeltaTable(path).to_pandas()
    parquet = pd.read_parquet(path, engine="pyarrow")

    print("Delta:  ", sorted(delta["id"].tolist()))
    print("Parquet:", sorted(parquet["id"].tolist()))
