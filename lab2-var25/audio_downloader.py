import os
import time
from typing import List, Dict, Optional
import requests


def download_audio_file(
    url: str, 
    download_folder: str, 
    filename: str,
    headers: Dict[str, str],
    timeout: int = 30
) -> Optional[Dict[str, str]]:
    """Скачивает один аудиофайл."""
    try:
        absolute_path = os.path.abspath(os.path.join(download_folder, filename))
        relative_path = os.path.relpath(absolute_path)

        audio_response = requests.get(url, headers=headers, timeout=timeout)
        audio_response.raise_for_status()

        is_valid_audio = (
            audio_response.headers.get('content-type') == 'audio/mpeg' 
            or len(audio_response.content) > 1000
        )

        if is_valid_audio:
            with open(absolute_path, 'wb') as f:
                f.write(audio_response.content)

            return {
                'filename': filename,
                'absolute_path': absolute_path,
                'relative_path': relative_path
            }
        else:
            print(f"✗ Файл слишком маленький или не MP3: {len(audio_response.content)} байт")
            return None

    except Exception as e:
        print(f"✗ Ошибка при скачивании {filename}: {e}")
        return None


def create_demo_files(download_folder: str, max_files: int) -> List[Dict[str, str]]:
    """Создает демо-файлы когда не удается скачать реальные."""
    audio_files_info = []
    
    demo_files = [
        "mixkit-piano-1.mp3", "mixkit-piano-2.mp3", "mixkit-piano-3.mp3",
        "mixkit-piano-4.mp3", "mixkit-piano-5.mp3", "mixkit-piano-6.mp3",
        "mixkit-piano-7.mp3", "mixkit-piano-8.mp3", "mixkit-piano-9.mp3",
        "mixkit-piano-10.mp3"
    ]

    for i, filename in enumerate(demo_files[:max_files]):
        absolute_path = os.path.abspath(os.path.join(download_folder, filename))
        relative_path = os.path.relpath(absolute_path)

        with open(absolute_path, 'w', encoding='utf-8') as f:
            f.write(f"Демо-файл: {filename}\n")
            f.write("Реальный файл с mixkit.co\n")
            f.write("Сайт блокирует прямое скачивание MP3\n")

        audio_files_info.append({
            'filename': filename,
            'absolute_path': absolute_path,
            'relative_path': relative_path
        })

    return audio_files_info


def download_piano_audio(
    urls: List[str],
    download_folder: str,
    max_files: int = 50
) -> List[Dict[str, str]]:
    """Скачивает аудиофайлы с пианино с mixkit.co."""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    audio_files_info: List[Dict[str, str]] = []
    downloaded_count = 0

    for i, audio_url in enumerate(urls[:max_files]):
        filename = f"piano_music_{i+1}.mp3"
        
        print(f"Скачивание {i+1}/{len(urls[:max_files])}: {filename}")
        
        file_info = download_audio_file(
            url=audio_url,
            download_folder=download_folder,
            filename=filename,
            headers=headers
        )
        
        if file_info:
            audio_files_info.append(file_info)
            downloaded_count += 1
            print(f"✓ Успешно скачан: {filename}")
        
        time.sleep(2)

    return audio_files_info