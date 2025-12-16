"""Модуль для обработки аудиофайлов."""
import numpy as np
import soundfile as sf


def increase_audio_speed(audio_data: np.ndarray, speed_factor: float) -> np.ndarray:
    """
    Увеличивает скорость аудиофайла в заданное количество раз.
    
    Args:
        audio_data: Массив аудиоданных
        speed_factor: Коэффициент увеличения скорости
        
    Returns:
        Ускоренный аудиомассив
        
    Raises:
        ValueError: Если speed_factor <= 0
    """
    if speed_factor <= 0:
        raise ValueError("Коэффициент скорости должен быть положительным числом")
    
    if len(audio_data.shape) == 1:
        return _process_mono_audio(audio_data, speed_factor)
    else:
        return _process_multi_channel_audio(audio_data, speed_factor)


def _process_mono_audio(audio_data: np.ndarray, speed_factor: float) -> np.ndarray:
    """Обрабатывает моно аудио."""
    original_length = len(audio_data)
    new_length = int(original_length / speed_factor)
    
    original_indices = np.arange(original_length)
    new_indices = np.linspace(0, original_length - 1, new_length)
    
    return np.interp(new_indices, original_indices, audio_data)


def _process_multi_channel_audio(audio_data: np.ndarray, 
                                speed_factor: float) -> np.ndarray:
    """Обрабатывает многоканальное аудио."""
    original_length = audio_data.shape[0]
    new_length = int(original_length / speed_factor)
    
    original_indices = np.arange(original_length)
    new_indices = np.linspace(0, original_length - 1, new_length)
    
    sped_up_audio = np.zeros((new_length, audio_data.shape[1]))
    for channel in range(audio_data.shape[1]):
        sped_up_audio[:, channel] = np.interp(
            new_indices, 
            original_indices, 
            audio_data[:, channel]
        )
    
    return sped_up_audio


def load_audio(file_path: str):
    """
    Загружает аудиофайл.
    
    Args:
        file_path: Путь к аудиофайлу
        
    Returns:
        tuple: (audio_data, samplerate)
        
    Raises:
        FileNotFoundError: Если файл не найден
        Exception: При ошибке загрузки файла
    """
    try:
        return sf.read(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не найден")
    except Exception as e:
        raise Exception(f"Ошибка при загрузке аудиофайла: {e}")


def save_audio(file_path: str, audio_data: np.ndarray, samplerate: int):
    """
    Сохраняет аудиофайл.
    
    Args:
        file_path: Путь для сохранения
        audio_data: Аудиоданные
        samplerate: Частота дискретизации
        
    Raises:
        Exception: При ошибке сохранения файла
    """
    try:
        sf.write(file_path, audio_data, samplerate)
    except Exception as e:
        raise Exception(f"Ошибка при сохранении аудиофайла: {e}")


def get_audio_info(audio_data: np.ndarray, samplerate: int) -> dict:
    """
    Получает информацию об аудиофайле.
    
    Args:
        audio_data: Аудиоданные
        samplerate: Частота дискретизации
        
    Returns:
        dict: Словарь с информацией об аудио
    """
    info = {
        "shape": audio_data.shape,
        "dtype": str(audio_data.dtype),
        "samplerate": samplerate,
        "duration": len(audio_data) / samplerate,
        "min_amplitude": float(audio_data.min()),
        "max_amplitude": float(audio_data.max()),
        "channels": 1 if len(audio_data.shape) == 1 else audio_data.shape[1],
        "samples": len(audio_data),
        "audio_type": "Моно" if len(audio_data.shape) == 1 else 
                     "Стерео" if audio_data.shape[1] == 2 else 
                     "Многоканальное"
    }
    return info