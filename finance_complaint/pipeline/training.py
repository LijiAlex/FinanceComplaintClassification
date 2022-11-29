import sys

from finance_complaint.exception import FinanceException
from finance_complaint.logger import logger
from finance_complaint.config.pipeline.training import FinanceConfig
from finance_complaint.entity.artifact_entity import *
from finance_complaint.component import DataIngestion, DataValidation, DataTransformation, ModelTrainer, \
ModelEvaluation, ModelPusher

class TrainingPipeline:

    def __init__(self, finance_config: FinanceConfig):
        self.finance_config: FinanceConfig = finance_config

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logger.info(f"\n{'#'*15}Data Ingestion Started{'#'*15}")
            data_ingestion_config = self.finance_config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info(f"\n{'#'*15}Data Ingestion Ended{'#'*15}")
            return data_ingestion_artifact
        except Exception as e:
            raise FinanceException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logger.info(f"\n{'#'*15}Data Validation Started{'#'*15}")
            data_validation_config = self.finance_config.get_data_validation_config()
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=data_validation_config)

            data_validation_artifact = data_validation.initiate_data_validation()
            logger.info(f"\n{'#'*15}Data Validation Ended{'#'*15}")
            return data_validation_artifact
        except Exception as e:
            raise FinanceException(e, sys)

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logger.info(f"\n{'#'*15}Data Transformation Started{'#'*15}")
            data_transformation_config = self.finance_config.get_data_transformation_config()
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=data_transformation_config
                                                     )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logger.info(f"\n{'#'*15}Data Transformation Ended{'#'*15}")
            return data_transformation_artifact
        except Exception as e:
            raise FinanceException(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logger.info(f"\n{'#'*15}Model Training Started{'#'*15}")
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.finance_config.get_model_trainer_config()
                                         )
            model_trainer_artifact = model_trainer.initiate_model_training()
            logger.info(f"\n{'#'*15}Model Training Ended{'#'*15}")
            return model_trainer_artifact
        except Exception as e:
            raise FinanceException(e, sys)

    def start_model_evaluation(self, data_validation_artifact, model_trainer_artifact) -> ModelEvaluationArtifact:
        try:
            logger.info(f"\n{'#'*15}Model evaluation started{'#'*15}")
            model_eval_config = self.finance_config.get_model_evaluation_config()
            model_eval = ModelEvaluation(data_validation_artifact=data_validation_artifact,
                                         model_trainer_artifact=model_trainer_artifact,
                                         model_eval_config=model_eval_config
                                         )
            model_eval_artifact =  model_eval.initiate_model_evaluation()
            logger.info(f"\n{'#'*15}Model evaluation Ended{'#'*15}")
            return model_eval_artifact
        except Exception as e:
            raise FinanceException(e, sys)

    def start_model_pusher(self, model_trainer_artifact: ModelTrainerArtifact):
        try:
            logger.info(f"\n{'#'*15}Model pusher started{'#'*15}")
            model_pusher_config = self.finance_config.get_model_pusher_config()
            model_pusher = ModelPusher(model_trainer_artifact=model_trainer_artifact,
                                       model_pusher_config=model_pusher_config
                                       )

            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logger.info(f"\n{'#'*15}Model pusher ended{'#'*15}")
            return model_pusher_artifact
        except Exception as e:
            raise FinanceException(e, sys)

    def start(self):
        try:
            logger.info(f"\n{'#'*15}Training Pipeline Started{'#'*15}")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                 data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_eval_artifact = self.start_model_evaluation(data_validation_artifact=data_validation_artifact,
                                                               model_trainer_artifact=model_trainer_artifact
                                                              )
            if model_eval_artifact.model_accepted:
                self.start_model_pusher(model_trainer_artifact=model_trainer_artifact)
            logger.info(f"\n{'#'*15}Training Pipeline Ended{'#'*15}")
        except Exception as e:
            raise FinanceException(e, sys)