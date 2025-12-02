from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float64, Int64, String

# 1. Define the entity
transaction_entity = Entity(
    name="transaction_id",
    join_keys=["transaction_id"],
    value_type=ValueType.STRING,  # mandatory now
)

# 2. Define the data source
transaction_source = FileSource(
    path="../data/transactions.parquet",   # relative to feature_repo/
    timestamp_field="event_timestamp"      # matches your parquet column
)

# 3. Define features
features = [Field(name=f"V{i}", dtype=Float64) for i in range(1, 29)]
features.append(Field(name="Amount", dtype=Float64))
features.append(Field(name="Class", dtype=Int64))       # fraud label
features.append(Field(name="location", dtype=String))   # categorical

# 4. Define the FeatureView
transaction_fv = FeatureView(
    name="transaction_features",
    entities=[transaction_entity],
    ttl=timedelta(days=7),
    schema=features,
    online=True,
    source=transaction_source,
    tags={},
)
