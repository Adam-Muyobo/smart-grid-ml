from pytorch_forecasting import TemporalFusionTransformer

def build_tft(dataset):
    return TemporalFusionTransformer.from_dataset(
        dataset,
        learning_rate=0.001,
        hidden_size=32,
        attention_head_size=4,
        dropout=0.1,
        loss="QuantileLoss",
        output_size=3  # 0.05, 0.5, 0.95
    )
