"""Точка входа в приложение для увеличения скорости аудио."""
import sys
import os
import argparse
from audio_processor import (
    load_audio,
    save_audio,
    increase_audio_speed,
    get_audio_info
)
from visualizer import create_comparison_plot


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description='Увеличение скорости аудиофайла'
    )
    
    parser.add_argument(
        'input_file',
        help='Имя аудиофайла из папки piano_music'
    )
    parser.add_argument(
        'output_file',
        help='Имя выходного файла'
    )
    parser.add_argument(
        'speed_factor',
        type=float,
        help='Коэффициент увеличения скорости (например: 2.0)'
    )
    
    return parser.parse_args()


def find_audio_file(filename: str) -> str:
    """
    Ищет аудиофайл по указанному пути.
    
    Args:
        filename: Имя файла или путь
        
    Returns:
        Полный путь к файлу
        
    Raises:
        FileNotFoundError: Если файл не найден
    """
    if os.path.exists(filename):
        return filename
    
    sounds_path = "../lab2-var25/piano_music/"
    alt_path = os.path.join(sounds_path, filename)
    
    if os.path.exists(alt_path):
        return alt_path
    
    raise FileNotFoundError(
        f"Файл '{filename}' не найден!\n"
        f"Проверенные пути:\n"
        f"1. {filename}\n"
        f"2. {alt_path}"
    )


def print_audio_statistics(info: dict, title: str):
    """
    Выводит статистику аудиофайла.
    
    Args:
        info: Словарь с информацией об аудио
        title: Заголовок для вывода
    """
    print(f"\n{'='*50}")
    print(title)
    print('='*50)
    print(f"Каналы: {info['channels']} ({'моно' if info['channels'] == 1 else 'стерео'})")
    print(f"Сэмплов: {info['samples']:,}")
    print(f"Частота дискретизации: {info['samplerate']} Hz")
    print(f"Длительность: {info['duration']:.2f} секунд")
    print(f"Размер массива: {info['shape']}")
    print(f"Тип данных: {info['dtype']}")
    print(f"Диапазон амплитуд: [{info['min_amplitude']:.4f}, {info['max_amplitude']:.4f}]")


def main():
    """Основная функция приложения."""
    args = parse_arguments()
    
    if args.speed_factor <= 0:
        print("Ошибка: Коэффициент скорости должен быть положительным числом.")
        sys.exit(1)
    
    try:
        input_path = find_audio_file(args.input_file)
        print(f"Загрузка аудиофайла: {input_path}")
        
        audio_data, samplerate = load_audio(input_path)
        
        original_info = get_audio_info(audio_data, samplerate)
        print_audio_statistics(original_info, "ИНФОРМАЦИЯ О ЗАГРУЖЕННОМ АУДИО")
        
        print(f"\nУвеличение скорости в {args.speed_factor} раз...")
        sped_up_audio = increase_audio_speed(audio_data, args.speed_factor)
        new_samplerate = int(samplerate * args.speed_factor)
        
        result_info = get_audio_info(sped_up_audio, new_samplerate)
        print_audio_statistics(result_info, "ИНФОРМАЦИЯ О РЕЗУЛЬТАТЕ")
        
        print(f"\nСохранение результата в файл: {args.output_file}")
        save_audio(args.output_file, sped_up_audio, new_samplerate)
        
        print("\nСоздание визуализации...")
        create_comparison_plot(
            audio_data,
            sped_up_audio,
            samplerate,
            new_samplerate,
            args.speed_factor
        )
        
        print(f"\n{'='*50}")
        print("ОБРАБОТКА ЗАВЕРШЕНА УСПЕШНО!")
        print('='*50)
        print(f"Исходный файл: {input_path}")
        print(f"Результат: {args.output_file}")
        print(f"Коэффициент скорости: {args.speed_factor}")
        print(f"Исходная длительность: {original_info['duration']:.2f} с")
        print(f"Новая длительность: {result_info['duration']:.2f} с")
        print(f"Сокращение: {original_info['duration'] - result_info['duration']:.2f} с")
        
    except FileNotFoundError as e:
        print(f"\nОШИБКА: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\nОШИБКА: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nНЕОЖИДАННАЯ ОШИБКА: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()