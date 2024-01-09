# model_train.py
import logging

from azureml.core import Run, Experiment,Workspace
from azureml.data import OutputFileDatasetConfig

from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration


ws = Workspace.from_config()


# Define logging
logger = logging.getLogger('azureml.core')
logger.setLevel(logging.DEBUG)


# Define environment and run config
env = ws.environments['mlops_01_env_from_pip_local']

# Create A Run Configuration
aml_run_config = RunConfiguration()
aml_run_config.target = "MLOps-01"  #The compute_targets available 
aml_run_config.environment = env  #The enviornmet 

# Define input/output datasets
load_data_step_path = OutputFileDatasetConfig(name="load_data_step")


# Load data step
load_step = PythonScriptStep(
    name="Load Data",
    source_directory="data_ingestion",
    script_name="load_data.py",
    arguments=["--output_path", load_data_step_path],
    outputs=[load_data_step_path],
    runconfig=aml_run_config
)


# Clean data step 
cleaned_data_step_path  = OutputFileDatasetConfig(name="clean_data_step")
clean_step = PythonScriptStep(
    name="Clean Data",
    source_directory="data_preprocessing",
    script_name="clean_data.py",
    arguments=["--input_path", load_data_step_path, "--output_path", cleaned_data_step_path],
    inputs=[load_data_step_path], 
    outputs=[cleaned_data_step_path],
    runconfig=aml_run_config,
    allow_reuse=True
)


# Linear Regression model step
lin_reg_model_step_path = OutputFileDatasetConfig(name="lin_reg_model_step")
lin_reg_model_step = PythonScriptStep(
  name="Train Linear Regression Model",
  source_directory="models",
  script_name="lin_reg_model.py",
  arguments=["--input_path", cleaned_data_step_path, "--output_path", lin_reg_model_step_path],
  inputs=[cleaned_data_step_path],
  outputs=[lin_reg_model_step_path],
  runconfig=aml_run_config
)


# Random forest model step
rf_model_step_path = OutputFileDatasetConfig(name="rf_model_step",)
rf_model_step = PythonScriptStep(
  name="Train RF Model",
  source_directory="models",
  script_name="rf_model.py",
  arguments=["--input_path", cleaned_data_step_path, "--output_path", rf_model_step_path],
  inputs=[cleaned_data_step_path],
  outputs=[rf_model_step_path],
  runconfig=aml_run_config
)



steps = [load_step, clean_step,lin_reg_model_step,rf_model_step]

model_train_pipeline = Pipeline(workspace=ws, steps=steps)
