from google.cloud import aiplatform
import hashlib
import json

def load_features(feature_store_id, entity_id, feature_ids):
    fs = aiplatform.Featurestore(feature_store_id)
    response = fs.read(
        entity_type_id="site",
        entity_ids=[entity_id],
        feature_ids=feature_ids
    )
    return response[0]

def compute_feature_hash(features: dict) -> str:
    canonical = json.dumps(features, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()
