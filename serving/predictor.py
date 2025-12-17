def predict(request):
    features = load_features(...)
    prediction = model.predict(features)
    return {
        "forecast": prediction["median"],
        "quantiles": prediction["quantiles"],
        "model_version": MODEL_VERSION,
        "input_features_hash": feature_hash
    }
