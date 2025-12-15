import argparse
import os
import time
from typing import List, Dict

import requests

from parser import parse_audio_urls_from_html
from audio_downloader import download_piano_audio, create_demo_files
from annotation import create_annotation_file
from iterator import AudioFileIterator


def collect_audio_urls(max_files: int = 50) -> List[str]:
    """Собирает аудио URL с разных страниц."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    urls = [
        "https://mixkit.co/free-stock-music/piano/",
        "https://mixkit.co/free-stock-music/tag/piano/",
        "https://mixkit.co/free-stock-music/classical/"
    ]

    all_audio_urls: List[str] = []

    for url in urls:
        if len(all_audio_urls) >= max_files:
            break

        print(f"Парсинг страницы: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            valid_urls = parse_audio_urls_from_html(response.content, "https://mixkit.co")
            all_audio_urls.extend(valid_urls)

            time.sleep(1)

        except Exception as e:
            print(f"Ошибка при парсинге {url}: {e}")
            continue

    all_audio_urls = list(set(all_audio_urls))
    print(f"Найдено уникальных аудио URL: {len(all_audio_urls)}")
    
    return all_audio_urls


def download_and_create_annotation(
    download_folder: str,
    annotation_file: str,
    max_files: int = 50
) -> int:
    """Основная функция для скачивания и создания аннотации."""
    
    os.makedirs(download_folder, exist_ok=True)
    
    audio_urls = collect_audio_urls(max_files)
    
    if not audio_urls:
        print("Не удалось найти аудио URL, создаем демо-файлы...")
        audio_files_info = create_demo_files(download_folder, max_files)
    else:
        audio_files_info = download_piano_audio(
            urls=audio_urls,
            download_folder=download_folder,
            max_files=max_files
        )
    
    if audio_files_info:
        create_annotation_file(audio_files_info, annotation_file)
        print(f"Аннотация сохранена в: {annotation_file}")
    
    return len(audio_files_info)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Скачивание аудиофайлов с пианино с mixkit.co'
    )
    parser.add_argument(
        '--download-folder', 
        type=str, 
        required=True, 
        help='Путь к папке для сохранения аудиофайлов'
    )
    parser.add_argument(
        '--annotation-file', 
        type=str, 
        required=True,
        help='Путь к файлу аннотации (CSV)'
    )
    parser.add_argument(
        '--max-files', 
        type=int, 
        default=50,
        help='Максимальное количество файлов для скачивания (по умолчанию: 50)'
    )

    args = parser.parse_args()

    print("=" * 50)
    print("Скачивание аудиофайлов с пианино с mixkit.co")
    print("=" * 50)

    downloaded_count = download_and_create_annotation(
        download_folder=args.download_folder,
        annotation_file=args.annotation_file,
        max_files=args.max_files
    )

    print(f"Итог: скачано/создано файлов: {downloaded_count}")

    if downloaded_count > 0:
        print("\n" + "=" * 50)
        print("Демонстрация работы итератора:")
        print("=" * 50)
        iterator = AudioFileIterator(args.annotation_file)

        for i, file_path in enumerate(iterator):
            print(f"  {i+1}. {file_path}")
    else:
        print("\nНе удалось скачать файлы.")


if __name__ == "__main__":
    main()