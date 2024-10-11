from Kidney_Disease_Classification import logger
from Kidney_Disease_Classification.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    # The `raise e` statement in the code snippet is re-raising the caught exception `e`. This means
    # that after logging the exception using the `logger.exception(e)` statement, the exception is
    # raised again to be handled by the higher-level exception handler or to terminate the program if
    # not caught at a higher level. This allows the exception to propagate up the call stack for
    # further handling or debugging.
    raise e