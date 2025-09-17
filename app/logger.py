import logging


class ConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        self._style = logging.PercentStyle("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        return super().format(record)
