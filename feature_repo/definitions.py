from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float64, Int64

# 1. Define an entity
# An entity is the business object that features are associated with.
transaction_entity = Entity(name="transaction_id", join_keys=["transaction_id"])

# 2. Define the Data Source
# This points to your Parquet file. Note the relative path from inside the
# feature_repo directory.
transaction_source = FileSource(
    path="../data/transactions.parquet",  # Path is relative to the feature_repo/ directory
    timestamp_field="event_timestamp" # Use 'timestamp_field' for newer versions
)

features = [Field(name=f"V{i}", dtype=Float64) for i in range(1, 29)]
features.append(Field(name="Amount", dtype=Float64))
# 3. Define the FeatureView
# A FeatureView groups related features together for a specific entity.
transaction_fv = FeatureView(
    name="transaction_features",
    entities=[transaction_entity],
    ttl=timedelta(days=7),
    schema=features,
    online=True,
    source=transaction_source,
    tags={},
)
