import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
# import dagshub
from Kidney_Disease_Classification.entity.config_entity import EvaluationConfig
from Kidney_Disease_Classification.utils.common import read_yaml,create_directories,save_json


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    
    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )


    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)
    

    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)
        self.save_score()

    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)

    
    # def log_into_mlflow(self):
    #     # Initialize DagsHub with your repo owner and repo name
    #     dagshub.init(repo_owner='mayank2393', repo_name='Kidney-Disease-Classification')
    #     mlflow.set_tracking_uri("https://dagshub.com/mayank2393/Kidney-Disease-Classification-MLflow-DVC.mlflow")
    #     # Start an MLflow run
    #     with mlflow.start_run():
    #         # Log parameters
    #         mlflow.log_params(self.config.all_params)

    #         # Log metrics
    #         mlflow.log_metrics(
    #             {"loss": self.score[0], "accuracy": self.score[1]}
    #         )

    #         # Register the model
    #         mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16Model")

# Example configuration structure