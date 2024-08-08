from src.etl.definitions import ProccessingType, Reader, Writer


class PipelineProperties:

    def __init__(
        self,
        reader: Reader,
        writer: Writer,
        processing_type: ProccessingType,
    ) -> None:
        self.reader = reader
        self.writer = writer
        self.processing_type = processing_type

    def get_reader(self) -> Reader:
        return self.reader

    def get_writer(self) -> Writer:
        return self.writer

    def get_processing_type(self) -> ProccessingType:
        return self.processing_type
