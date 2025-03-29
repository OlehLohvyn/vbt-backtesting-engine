"""
binance_loader.py

Implementation of BaseLoader for downloading spot market data from Binance
using the public data archive (https://data.binance.vision).
"""

import urllib.request
from pathlib import Path

from core.data_loader.base_loader.base_loader import BaseLoader
from core.data_loader.binance_loader.binance_constants import BASE_URL
from exceptions.data_loader import DataLoaderError
from settings import STORE_DIRECTORY
from utils.logging_config import logger


class BinanceLoader(BaseLoader):
    """
    Data loader for Binance spot market. Builds data paths and downloads files
    from Binance's public archive.
    """

    def get_path(
        self,
        market_data_type: str,
        time_period: str,
        symbol: str,
        interval: str
    ) -> str:
        """
        Construct a relative path to the data file based on Binance directory structure.

        Args:
            market_data_type: e.g. 'klines', 'aggTrades'.
            time_period: e.g. 'daily', 'monthly'.
            symbol: e.g. 'BTCUSDT'.
            interval: e.g. '1m', '1h'.

        Returns:
            Relative path string (e.g. 'spot/daily/klines/BTCUSDT/1m/').
        """
        symbol = symbol.upper()
        path_parts = ['spot', time_period, market_data_type, symbol, interval]
        return '/'.join(path_parts) + '/'

    def get_download_url(self, file_url: str) -> str:
        """
        Build the full download URL.

        Args:
            file_url: Relative path and filename.

        Returns:
            Full URL to download the file.
        """
        return f"{BASE_URL}data/{file_url}"

    def download_file(
        self,
        relative_path: str,
        file_name: str,
        folder: str = STORE_DIRECTORY
    ) -> None:
        """
        Download a file and save it locally.

        Args:
            relative_path: Path relative to base archive.
            file_name: File name (e.g. 'BTCUSDT-1m-2025-02-01.zip').
            folder: Target folder to store the file.

        Returns:
            None
        """
        file_path = self._build_file_path(folder, relative_path, file_name)
        self._ensure_directory_exists(file_path)

        if file_path.exists():
            logger.info(f"File already exists: {file_path}")
            return

        download_url = self.get_download_url(f"{relative_path}{file_name}")
        logger.info(f"Starting download: {download_url}")

        try:
            self._download_to_file(download_url, file_path)
            logger.info(f"Download completed: {file_path}")
        except urllib.error.HTTPError:
            self._handle_download_error(f"File not found: {download_url}", download_url)
        except Exception as e:
            self._handle_download_error(f"Unexpected error while downloading {download_url}", download_url, e)

    # ──────────────────────── PRIVATE METHODS ────────────────────────

    def _build_file_path(self, folder: str, relative_path: str, file_name: str) -> Path:
        return Path(folder) / relative_path / file_name

    def _ensure_directory_exists(self, file_path: Path) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)

    def _download_to_file(self, url: str, path: Path) -> None:
        with urllib.request.urlopen(url) as response, open(path, 'wb') as out_file:
            length = response.getheader('content-length')
            total_size = int(length) if length else None
            blocksize = self._calculate_blocksize(length)

            downloaded = 0
            last_logged_percent = 0

            while True:
                buf = response.read(blocksize)
                if not buf:
                    break
                out_file.write(buf)
                downloaded += len(buf)

                if total_size:
                    percent = int(downloaded * 100 / total_size)
                    if percent >= last_logged_percent + 10:
                        logger.info(f"Downloading... {percent}%")
                        last_logged_percent = percent

    def _calculate_blocksize(self, length: str | None) -> int:
        return max(4096, int(length) // 100) if length else 4096

    def _handle_download_error(
        self,
        message: str,
        url: str,
        exception: Exception | None = None
    ) -> None:
        logger.error(message)
        if exception:
            logger.exception(exception)
        raise DataLoaderError(f"Download error for URL: {url}") from exception
