from src.database.schema.updater import DatabaseSchemaUpdater
from src.etl.core.definitions import Format, Layer
from src.etl.core.pipeline import Pipeline
from src.etl.engines import CleaningEngine, ExtractionEngine, RefinementEngine
from src.etl.io import IOHandler


def orchestrate_etl_process(update_schema: bool = True) -> None:

    extraction_pipeline = Pipeline(
        reader=IOHandler(layer=Layer.DATABASE, format=Format.JDBC),
        engine=ExtractionEngine(),
        writer=IOHandler(layer=Layer.BRONZE, format=Format.PARQUET),
    )
    cleaning_pipeline = Pipeline(
        reader=IOHandler(layer=Layer.BRONZE, format=Format.PARQUET),
        engine=CleaningEngine(),
        writer=IOHandler(layer=Layer.SILVER, format=Format.DELTA),
    )
    refinement_pipeline = Pipeline(
        reader=IOHandler(layer=Layer.SILVER, format=Format.DELTA),
        engine=RefinementEngine(),
        writer=IOHandler(layer=Layer.GOLD, format=Format.DELTA),
    )

    if update_schema:
        schema_updater = DatabaseSchemaUpdater()
        schema_updater.update_element_schemas()

    extraction_pipeline.execute()
    cleaning_pipeline.execute()
    refinement_pipeline.execute()


if __name__ == "__main__":
    orchestrate_etl_process()
