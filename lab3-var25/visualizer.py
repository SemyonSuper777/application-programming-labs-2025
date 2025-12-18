"""Модуль для визуализации аудиоданных."""
import numpy as np
import matplotlib.pyplot as plt


def create_comparison_plot(original_audio: np.ndarray,
                          sped_up_audio: np.ndarray,
                          original_samplerate: int,
                          sped_up_samplerate: int,
                          speed_factor: float):
    """
    Создает график сравнения оригинального и ускоренного аудио.
    
    Args:
        original_audio: Оригинальное аудио
        sped_up_audio: Ускоренное аудио
        original_samplerate: Частота дискретизации оригинального аудио
        sped_up_samplerate: Частота дискретизации ускоренного аудио
        speed_factor: Коэффициент увеличения скорости
    """
    samples_to_show_original = min(len(original_audio), 
                                   int(original_samplerate * 2))
    samples_to_show_sped_up = min(len(sped_up_audio), 
                                  int(sped_up_samplerate * 2))
    
    time_original = np.arange(samples_to_show_original) / original_samplerate
    time_sped_up = np.arange(samples_to_show_sped_up) / sped_up_samplerate
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    if len(original_audio.shape) == 1:
        ax1.plot(time_original, original_audio[:samples_to_show_original], 
                'b-', alpha=0.7, linewidth=0.8)
        ax2.plot(time_sped_up, sped_up_audio[:samples_to_show_sped_up], 
                'r-', alpha=0.7, linewidth=0.8)
    else:
        ax1.plot(time_original, original_audio[:samples_to_show_original, 0], 
                'b-', alpha=0.7, linewidth=0.8)
        ax2.plot(time_sped_up, sped_up_audio[:samples_to_show_sped_up, 0], 
                'r-', alpha=0.7, linewidth=0.8)
    
    ax1.set_title(f'Оригинальное аудио ({len(original_audio)} сэмплов, '
                 f'{len(original_audio)/original_samplerate:.2f} с)')
    ax2.set_title(f'Ускоренное аудио (x{speed_factor}, {len(sped_up_audio)} сэмплов, '
                 f'{len(sped_up_audio)/sped_up_samplerate:.2f} с)')
    
    for ax in (ax1, ax2):
        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Амплитуда')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-1.1, 1.1)
    
    plt.tight_layout()
    plt.show()