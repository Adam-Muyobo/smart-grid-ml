from kfp.v2 import dsl

@dsl.pipeline(name="forecast-training-pipeline")
def training_pipeline():
    dataset = build_dataset_op()
    model = train_model_op(dataset)
    eval = evaluate_model_op(model)
    register_model_op(model, eval)
