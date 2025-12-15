import csv
import os
from typing import List, Dict


def create_annotation_file(
    audio_files_info: List[Dict[str, str]],
    annotation_file: str
) -> None:
    """Создает файл аннотации из списка информации о файлах."""
    with open(annotation_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'absolute_path', 'relative_path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for info in audio_files_info:
            writer.writerow(info)


def load_annotation(annotation_file: str) -> List[str]:
    """Загружает аннотацию из CSV файла и возвращает список путей."""
    audio_files: List[str] = []
    try:
        with open(annotation_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                audio_files.append(row['absolute_path'])
    except FileNotFoundError:
        print(f"Файл аннотации {annotation_file} не найден")
    return audio_files