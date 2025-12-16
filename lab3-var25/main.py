"""Увеличение скорости аудиофайлов."""
import sys
import os
import argparse
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


def speed_up_audio(audio, speed_factor):
    """Увеличивает скорость аудио."""
    if speed_factor <= 0:
        raise ValueError("Коэффициент скорости должен быть > 0")
    
    if len(audio.shape) == 1:
        old_len = len(audio)
        new_len = int(old_len / speed_factor)
        return np.interp(np.linspace(0, old_len-1, new_len), 
                        np.arange(old_len), audio)
    else:
        old_len = audio.shape[0]
        new_len = int(old_len / speed_factor)
        result = np.zeros((new_len, audio.shape[1]))
        for i in range(audio.shape[1]):
            result[:, i] = np.interp(np.linspace(0, old_len-1, new_len),
                                   np.arange(old_len), audio[:, i])
        return result


def show_plot(orig, new, sr_orig, sr_new, factor):
    """Показывает график сравнения."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    samples_orig = min(len(orig), int(sr_orig * 2))
    samples_new = min(len(new), int(sr_new * 2))
    
    time_orig = np.arange(samples_orig) / sr_orig
    time_new = np.arange(samples_new) / sr_new
    
    if len(orig.shape) == 1:
        ax1.plot(time_orig, orig[:samples_orig], 'b-', alpha=0.7, linewidth=0.8)
        ax2.plot(time_new, new[:samples_new], 'r-', alpha=0.7, linewidth=0.8)
    else:
        ax1.plot(time_orig, orig[:samples_orig, 0], 'b-', alpha=0.7, linewidth=0.8)
        ax2.plot(time_new, new[:samples_new, 0], 'r-', alpha=0.7, linewidth=0.8)
    
    ax1.set_title(f'Оригинал ({len(orig)} сэмплов, {len(orig)/sr_orig:.1f}с)')
    ax2.set_title(f'Ускоренное x{factor} ({len(new)} сэмплов, {len(new)/sr_new:.1f}с)')
    
    for ax in [ax1, ax2]:
        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Амплитуда')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-1.1, 1.1)
    
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Увеличение скорости аудио')
    parser.add_argument('input', help='Имя аудиофайла из папки piano_music')
    parser.add_argument('output', help='Выходной файл')
    parser.add_argument('factor', type=float, help='Коэффициент скорости')
    
    args = parser.parse_args()
    
    SOUNDS_PATH = "../lab2-var25/piano_music/"
    
    if not os.path.exists(args.input):
        alt_path = os.path.join(SOUNDS_PATH, args.input)
        if os.path.exists(alt_path):
            args.input = alt_path
        else:
            print(f"Файл '{args.input}' не найден!")
            print(f"Искал в: {alt_path}")
            print(f"Папка существует: {os.path.exists(SOUNDS_PATH)}")
            sys.exit(1)
    
    if args.factor <= 0:
        print("Ошибка: коэффициент скорости должен быть > 0")
        sys.exit(1)
    
    try:
        print(f"Загрузка: {args.input}")
        audio, sr = sf.read(args.input)
        
        print(f"Размер: {audio.shape}")
        print(f"Тип: {'моно' if len(audio.shape)==1 else 'стерео'}")
        print(f"Сэмплов: {len(audio):,}")
        print(f"Частота: {sr} Hz")
        print(f"Длительность: {len(audio)/sr:.2f} сек")
        
        print(f"\nУскоряем в {args.factor} раз...")
        new_audio = speed_up_audio(audio, args.factor)
        new_sr = int(sr * args.factor)
        
        print(f"Сохранение: {args.output}")
        sf.write(args.output, new_audio, new_sr)
        
        print("\nГрафик...")
        show_plot(audio, new_audio, sr, new_sr, args.factor)
        
        print("\nГотово!")
        print(f"Исходно: {len(audio)/sr:.2f} сек")
        print(f"Результат: {len(new_audio)/new_sr:.2f} сек")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()