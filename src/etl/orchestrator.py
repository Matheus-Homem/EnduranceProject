from src.database.schema.updater import DatabaseSchemaUpdater
from src.etl.core.definitions import Format, Layer
from src.etl.core.pipeline import Pipeline
from src.etl.engines import CleaningEngine, ExtractionEngine, RefinementEngine
from src.etl.io.manager import IOManager


def orchestrate_etl_process(refresh_schema: bool = True) -> None:

    extraction_pipeline = Pipeline(
        reader=IOManager(layer=Layer.DATABASE, format=Format.JDBC),
        engine=ExtractionEngine(),
        writer=IOManager(layer=Layer.BRONZE, format=Format.PARQUET),
    )
    cleaning_pipeline = Pipeline(
        reader=IOManager(layer=Layer.BRONZE, format=Format.PARQUET),
        engine=CleaningEngine(),
        writer=IOManager(layer=Layer.SILVER, format=Format.DELTA),
    )
    refinement_pipeline = Pipeline(
        reader=IOManager(layer=Layer.SILVER, format=Format.DELTA),
        engine=RefinementEngine(),
        writer=IOManager(layer=Layer.GOLD, format=Format.DELTA),
    )

    if refresh_schema:
        schema_updater = DatabaseSchemaUpdater()
        schema_updater.update_element_schemas()

    extraction_pipeline.execute(table_to_read="element_entries", table_to_write="entries")
    extraction_pipeline.execute(table_to_read="element_schemas", table_to_write="schemas")
    cleaning_pipeline.execute(table_to_read="entries")
    refinement_pipeline.execute()


if __name__ == "__main__":
    orchestrate_etl_process()
