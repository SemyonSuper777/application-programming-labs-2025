"""Модуль для обработки аудиофайлов."""
import numpy as np
import soundfile as sf


def load_audio(file_path: str):
    """
    Загружает аудиофайл.
    
    Args:
        file_path: Путь к аудиофайлу
        
    Returns:
        tuple: (audio_data, samplerate)
    """
    try:
        return sf.read(file_path)
    except Exception as e:
        raise Exception(f"Ошибка при загрузке аудиофайла: {e}")


def save_audio(file_path: str, audio_data: np.ndarray, samplerate: int):
    """
    Сохраняет аудиофайл.
    
    Args:
        file_path: Путь для сохранения
        audio_data: Аудиоданные
        samplerate: Частота дискретизации
    """
    try:
        sf.write(file_path, audio_data, samplerate)
    except Exception as e:
        raise Exception(f"Ошибка при сохранении аудиофайла: {e}")


def increase_audio_speed(audio_data: np.ndarray, speed_factor: float) -> np.ndarray:
    """
    Увеличивает скорость аудиофайла в заданное количество раз.
    
    Args:
        audio_data: Массив аудиоданных
        speed_factor: Коэффициент увеличения скорости
        
    Returns:
        Ускоренный аудиомассив
    """
    if speed_factor <= 0:
        raise ValueError("Коэффициент скорости должен быть > 0")
    
    if len(audio_data.shape) == 1:
        return _process_mono_audio(audio_data, speed_factor)
    return _process_stereo_audio(audio_data, speed_factor)


def _process_mono_audio(audio_data: np.ndarray, speed_factor: float) -> np.ndarray:
    """Обрабатывает моно аудио."""
    old_len = len(audio_data)
    new_len = int(old_len / speed_factor)
    return np.interp(
        np.linspace(0, old_len - 1, new_len),
        np.arange(old_len),
        audio_data
    )


def _process_stereo_audio(audio_data: np.ndarray, speed_factor: float) -> np.ndarray:
    """Обрабатывает стерео аудио."""
    old_len = audio_data.shape[0]
    new_len = int(old_len / speed_factor)
    
    result = np.zeros((new_len, audio_data.shape[1]))
    for channel in range(audio_data.shape[1]):
        result[:, channel] = np.interp(
            np.linspace(0, old_len - 1, new_len),
            np.arange(old_len),
            audio_data[:, channel]
        )
    return result


def get_audio_info(audio_data: np.ndarray, samplerate: int) -> dict:
    """
    Получает информацию об аудиофайле.
    
    Args:
        audio_data: Аудиоданные
        samplerate: Частота дискретизации
        
    Returns:
        dict: Информация об аудио
    """
    duration = len(audio_data) / samplerate
    
    return {
        "channels": 1 if len(audio_data.shape) == 1 else audio_data.shape[1],
        "samples": len(audio_data),
        "samplerate": samplerate,
        "duration": duration,
        "shape": audio_data.shape,
        "dtype": str(audio_data.dtype),
        "min_amplitude": float(audio_data.min()),
        "max_amplitude": float(audio_data.max())
    }