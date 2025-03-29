from abc import ABC, abstractmethod

class BaseLoader(ABC):
    """
    @abstractmethod
    def get_path(self, market_data_type, time_period, symbol, interval=None):
        pass

    @abstractmethod
    def get_download_url(self, file_url: str) -> str:
        pass

    @abstractmethod
    def download_file(self, relative_path: str, file_name: str, folder: str = None):
        pass
"""