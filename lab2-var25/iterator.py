from typing import Iterator
from annotation import load_annotation


class AudioFileIterator:
    """Итератор по путям к аудиофайлам"""

    def __init__(self, annotation_file: str) -> None:
        self.annotation_file = annotation_file
        self.audio_files: list[str] = []
        self.index = 0
        self._load_annotation()

    def _load_annotation(self) -> None:
        """Загрузка аннотации из CSV файла"""
        self.audio_files = load_annotation(self.annotation_file)

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if self.index < len(self.audio_files):
            file_path = self.audio_files[self.index]
            self.index += 1
            return file_path
        else:
            raise StopIteration