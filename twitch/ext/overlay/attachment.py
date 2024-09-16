"""
The MIT License (MIT)

Copyright (c) 2024-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT firstED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import gzip
import io

if TYPE_CHECKING:
    from typing import Optional, Dict

import logging
_logger = logging.getLogger(__name__)


class Attachment:
    """
    Manages file attachments in memory, including loading, compressing,
    decompressing, and retrieving files.
    """

    __slots__ = ('attachments', 'path_keys')

    def __init__(self) -> None:
        self.attachments: Dict[str, bytes] = {}
        self.path_keys: Dict[str, str] = {}

    def clear(self) -> None:
        """Clears all attachments and path keys from memory."""
        self.attachments.clear()
        self.path_keys.clear()
        _logger.debug('All attachments have been cleared from memory.')

    @staticmethod
    def compress_data(data: bytes) -> bytes:
        """Compresses data using gzip."""
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode='wb') as gzip_file:
            gzip_file.write(data)
        return buffer.getvalue()

    @staticmethod
    def decompress_data(compressed_data: bytes) -> bytes:
        """Decompresses gzip-compressed data."""
        buffer = io.BytesIO(compressed_data)
        with gzip.GzipFile(fileobj=buffer, mode='rb') as gzip_file:
            return gzip_file.read()

    @staticmethod
    def convert_path_to_key(path: str) -> str:
        """Converts a file path to a hash-based key with the file extension."""
        ext = f'.{path.rsplit(".", 1)[-1]}' if '.' in path else ''
        key = f"{abs(hash(path))}{ext}"
        _logger.debug('Converted path `%s` to key `%s`.', path, key)
        return key

    def load_file_into_memory(self, name: str, path: str) -> None:
        """Loads a file from the filesystem into memory and compresses it."""
        with open(path, 'rb') as file:
            file_data = file.read()
            compressed_data = self.compress_data(file_data)
            path_key = self.convert_path_to_key(path)
            self.attachments[path_key] = compressed_data
            self.path_keys[name] = path_key
        _logger.debug('File `%s` loaded into memory with name `%s`.', path, name)

    def get_attachment(self, path_key: str) -> Optional[bytes]:
        """Retrieves and decompresses a file from memory."""
        compressed_file_content = self.attachments.get(path_key)
        if compressed_file_content:
            return self.decompress_data(compressed_file_content)
        return None

    def get_path_key(self, name: str) -> Optional[str]:
        """Retrieves the path key for a given name."""
        return self.path_keys.get(name, name)

    def remove_attachment(self, name: str) -> None:
        """Removes a file from memory based on its name."""
        try:
            if name in self.path_keys:
                path_key = self.path_keys.pop(name)
                self.attachments.pop(path_key, None)
                _logger.debug('Removed attachment with name `%s`.', name)
        except Exception as exc:
            _logger.exception('Failed to remove attachment', exc)
