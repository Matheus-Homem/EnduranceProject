from src.etl.definitions import GoldTable, Pipeline
from src.etl.readers.delta import DeltaReader
from src.etl.writers.delta import DeltaWriter


class RefinerPipeline(Pipeline):

    @staticmethod
    def execute(
        table: GoldTable,
        reader=DeltaReader(),
        writer=DeltaWriter(),
    ) -> None:
        dataframe = reader.read_dataframe(source=table.source.get_path())
        writer.write_dataframe(dataframe=dataframe, path=table.get_path())
