from src.etl.definitions import PipelineDefinition


def execute_pipeline(pipeline_definitions: PipelineDefinition):
    reader = pipeline_definitions.get_reader()
    writer = pipeline_definitions.get_writer()

    df = reader.read_data()
    writer.write_data(df)
