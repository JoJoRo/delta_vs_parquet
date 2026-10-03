from pathlib import Path
from tempfile import TemporaryDirectory

import pyarrow as pa
import pyarrow.parquet as pq
from deltalake import DeltaTable, write_deltalake


with TemporaryDirectory() as tmp:
    path = Path(tmp) / "example"

    def read_delta():
        table = DeltaTable(str(path)).to_pyarrow_table()
        return sorted(table.column("id").to_pylist())

    def read_parquet():
        # Read data files directly, ignoring the Delta transaction log.
        files = [str(p) for p in path.glob("*.parquet")]
        table = pq.read_table(files)
        return sorted(table.column("id").to_pylist())

    write_deltalake(str(path), pa.table({"id": [1, 2]}))

    print("Initially:")
    print("  Delta:  ", read_delta())
    print("  Parquet:", read_parquet())

    # Replace the logical table. Old files remain until cleaned up.
    write_deltalake(
        str(path),
        pa.table({"id": [2, 3]}),
        mode="overwrite",
    )

    print("After overwrite:")
    print("  Delta:  ", read_delta())
    print("  Parquet:", read_parquet())

    assert read_delta() == [2, 3]
    assert read_parquet() == [1, 2, 2, 3]
