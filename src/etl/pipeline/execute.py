from src.etl.definitions import ProccessingType
from src.etl.pipeline.properties import PipelineProperties
from src.etl.processes.full import full_processing
from src.etl.processes.incremental import incremental_processing


def execute_pipeline(pipeline_properties: PipelineProperties):
    reader = pipeline_properties.get_reader()
    writer = pipeline_properties.get_writer()
    processing_type = pipeline_properties.get_processing_type()

    processing_dict = {
        ProccessingType.FULL: full_processing,
        ProccessingType.INCREMENTAL: incremental_processing,
    }

    df = reader.read()
    df = processing_dict[processing_type](df)
    writer.write(df)
