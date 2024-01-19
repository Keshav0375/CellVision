import os, sys
import zipfile
import shutil
import yaml
from cellSegmentation.utils.main_utils import read_yaml_file
from cellSegmentation.logger import logging
from cellSegmentation.exception import AppException
from cellSegmentation.entity.config_entity import ModelTrainerConfig
from cellSegmentation.entity.artifacts_entity import ModelTrainerArtifact


class ModelTrainer:
    def __init__(
            self,
            model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self, ) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            logging.info("Unzipping data")
            # Specify the path to the zip file
            zip_file_path = "data.zip"

            # Specify the directory where you want to extract the contents
            extract_to_directory = r"C:\Users\kesha\PycharmProjects\segment\CellVision"

            # Open the zip file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                # Extract all contents to the specified directory
                zip_ref.extractall(extract_to_directory)

            # Optionally, remove the zip file after extraction
            os.remove(zip_file_path)

            os.system(
                f"yolo task=segment mode=train model={self.model_trainer_config.weight_name} data=data.yaml epochs={self.model_trainer_config.no_epochs} imgsz=640 save=true")

            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            os.system(f"cp runs/segment/train/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")

            os.remove("yolov8s-seg.pt")
            shutil.rmtree("train")
            shutil.rmtree("valid")
            shutil.rmtree("test")
            os.remove("data.yaml")
            shutil.rmtree("runs")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="artifacts/model_trainer/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact


        except Exception as e:
            raise AppException(e, sys)

