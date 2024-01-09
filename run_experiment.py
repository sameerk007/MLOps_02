# run_experiment.py

from azureml.core import Workspace, Experiment , Model
from aml_pipelines.model_train import model_train_pipeline
from azureml.core import Run
from azureml.data import OutputFileDatasetConfig

# Load Azure ML workspace
ws = Workspace.from_config()

# Create an experiment
experiment = Experiment(ws, "housing-pipeline")

# Validate the pipeline
model_train_pipeline.validate()

# Publish the pipeline
published_pipeline = model_train_pipeline.publish(name="housing-pipeline")

# Submit the pipeline to the experiment
pipeline_run = Experiment(ws, "housing-price-prediction").submit(published_pipeline)

# Wait for the pipeline run to complete
pipeline_run.wait_for_completion(show_output=True)

# Get the best model
def get_best_model(pipeline_run):


    print ("#_________#___________#___________")
    # best_r2_score = -float('inf')  # Initialize with negative infinity
    # best_model_step = ""

    # Get the step run associated with the step name
    for model_step in ['Train Linear Regression Model', 'Train RF Model']:
        step_runs = pipeline_run.find_step_run(model_step)
        for step in step_runs:
            print(f"Step Name: {step.name}")
            print(f"Run ID: {step.id}")
        
        # Access the run associated with the step
        run = Run(run_id=step.id, experiment=step.experiment)

        # Retrieve and print the logged metrics
        metrics = run.get_metrics()
        print("Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value}")
        print("#----#OVER------#")


    #     # Access the run associated with the step
    #     run = Run(run_id=step_run.id, experiment=step_run.experiment)

    #     # Retrieve the R2 score from the metrics
    #     metrics = run.get_metrics()
    #     r2_score = metrics.get('r2', None)

    #     # Print the metrics
    #     print(f"Metrics for {model_step}:")
    #     for key, value in metrics.items():
    #         print(f"{key}: {value}")

    #     # Check if the current model has a better R2 score
    #     if r2_score is not None and r2_score > best_r2_score:
    #         best_r2_score = r2_score
    #         best_model_step = model_step

    # # Print the best model based on R2 score
    # if best_model_step:
    #     print(f"\nBest model based on R2 score: {best_model_step} with R2 score: {best_r2_score}")

    #     # Get the model path using OutputFileDatasetConfig
    #     model_output_path = step_run.get_output_data(best_model_step).as_mount() + "/outputs/model.pkl"

    #     # Register the best model
    #     model = Model.register(workspace=ws,
    #                            model_path=model_output_path,
    #                            model_name=best_model_step,
    #                            description=f"Best model based on R2 score: {best_r2_score}")

    #     print(f"Model registered: {model.name}, Version: {model.version}")
    # else:
    #     print("No models found with valid R2 scores.")

# Call the function to get metrics and register the best model
get_best_model(pipeline_run)
