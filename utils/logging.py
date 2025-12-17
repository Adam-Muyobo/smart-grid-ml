def log_prediction(bq_client, record):
    bq_client.insert_rows_json(
        "audit.forecast_predictions",
        [record]
    )