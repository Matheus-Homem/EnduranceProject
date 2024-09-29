from src.database.schema.updater import DatabaseSchemaUpdater
from src.etl.definitions import Layer
from src.etl.engines.cleaning import CleaningEngine
from src.etl.engines.extraction import ExtractionEngine
from src.etl.engines.refinement import RefinementEngine
from src.etl.io.database import DatabaseReader
from src.etl.io.delta import DeltaHandler
from src.etl.io.parquet import ParquetHandler
from src.etl.pipeline import Pipeline


def orchestrate_etl_process():
    extraction_pipeline = Pipeline(
        reader=DatabaseReader(layer=Layer.DATABASE),
        engine=ExtractionEngine(),
        writer=ParquetHandler(layer=Layer.BRONZE),
    )
    cleaning_pipeline = Pipeline(
        reader=ParquetHandler(layer=Layer.BRONZE),
        engine=CleaningEngine(),
        writer=DeltaHandler(layer=Layer.SILVER),
    )
    refinement_pipeline = Pipeline(
        reader=DeltaHandler(layer=Layer.SILVER),
        engine=RefinementEngine(),
        writer=DeltaHandler(layer=Layer.GOLD),
    )
    schema_updater = DatabaseSchemaUpdater()
    schema_updater.update_element_schemas()
    extraction_pipeline.execute()
    cleaning_pipeline.execute()
    refinement_pipeline.execute()


if __name__ == "__main__":
    orchestrate_etl_process()
