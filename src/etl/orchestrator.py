from src.database.schema.updater import DatabaseSchemaUpdater
from src.etl.core.definitions import Layer
from src.etl.core.entity import EntityDTO
from src.etl.core.pipeline import Pipeline
from src.etl.engines.cleaning import CleaningEngine
from src.etl.engines.extraction import ExtractionEngine
from src.etl.engines.refinement import RefinementEngine
from src.etl.io.database import DatabaseHandler
from src.etl.io.delta import DeltaHandler
from src.etl.io.parquet import ParquetHandler


def orchestrate_etl_process(update_schema: bool = True) -> None:

    extraction_pipeline = Pipeline(
        reader=DatabaseHandler(layer=Layer.DATABASE),
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

    if update_schema:
        schema_updater = DatabaseSchemaUpdater()
        schema_updater.update_element_schemas()

    entity_dto = EntityDTO()

    extraction_pipeline.set_entity(entity=entity_dto)
    extraction_pipeline.execute()
    cleaning_pipeline.execute()
    refinement_pipeline.execute()


if __name__ == "__main__":
    orchestrate_etl_process()
