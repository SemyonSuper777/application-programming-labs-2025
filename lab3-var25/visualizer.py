"""Модуль для визуализации аудиоданных."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def plot_audio_comparison(original_audio: np.ndarray,
                         sped_up_audio: np.ndarray,
                         original_samplerate: int,
                         sped_up_samplerate: int,
                         speed_factor: float,
                         duration_seconds: float = 5) -> None:
    """
    Создает график сравнения оригинального и ускоренного аудио.
    
    Args:
        original_audio: Оригинальное аудио
        sped_up_audio: Ускоренное аудио
        original_samplerate: Частота дискретизации оригинального аудио
        sped_up_samplerate: Частота дискретизации ускоренного аудио
        speed_factor: Коэффициент увеличения скорости
        duration_seconds: Продолжительность отображаемого сегмента в секундах
    """
    samples_to_show_original = min(
        len(original_audio),
        int(original_samplerate * duration_seconds)
    )
    samples_to_show_sped_up = min(
        len(sped_up_audio),
        int(sped_up_samplerate * duration_seconds)
    )
    
    time_original = np.arange(samples_to_show_original) / original_samplerate
    time_sped_up = np.arange(samples_to_show_sped_up) / sped_up_samplerate
    
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(3, 2, figure=fig, height_ratios=[2, 2, 1])
    
    colors = ['blue', 'red']
    
    if len(original_audio.shape) == 1:
        _plot_mono_comparison(fig, gs, colors,
                             original_audio, sped_up_audio,
                             time_original, time_sped_up,
                             samples_to_show_original,
                             samples_to_show_sped_up)
    else:
        _plot_multi_channel_comparison(fig, gs, colors,
                                      original_audio, sped_up_audio,
                                      time_original, time_sped_up,
                                      samples_to_show_original,
                                      samples_to_show_sped_up)
    
    _add_info_panel(fig, gs, original_audio, sped_up_audio,
                   original_samplerate, sped_up_samplerate,
                   speed_factor)
    
    plt.suptitle(
        f'Сравнение оригинального и ускоренного аудио (коэффициент: {speed_factor})',
        fontsize=16,
        fontweight='bold'
    )
    plt.tight_layout()
    plt.show()


def _plot_mono_comparison(fig, gs, colors,
                         original_audio, sped_up_audio,
                         time_original, time_sped_up,
                         samples_orig, samples_sped):
    """Создает график для моно аудио."""
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(
        time_original,
        original_audio[:samples_orig],
        color=colors[0],
        linewidth=0.8,
        label=f'Оригинал ({len(original_audio)} сэмплов)'
    )
    ax1.set_title('Оригинальное аудио (моно)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Время (секунды)')
    ax1.set_ylabel('Амплитуда')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_ylim([-1.1, 1.1])
    
    ax2 = fig.add_subplot(gs[1, :])
    ax2.plot(
        time_sped_up,
        sped_up_audio[:samples_sped],
        color=colors[1],
        linewidth=0.8,
        label=f'Ускоренное ({len(sped_up_audio)} сэмплов)'
    )
    ax2.set_title('Ускоренное аудио (моно)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Время (секунды)')
    ax2.set_ylabel('Амплитуда')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_ylim([-1.1, 1.1])


def _plot_multi_channel_comparison(fig, gs, colors,
                                  original_audio, sped_up_audio,
                                  time_original, time_sped_up,
                                  samples_orig, samples_sped):
    """Создает график для многоканального аудио."""
    channels = original_audio.shape[1]
    channel_names = (
        ['Левый канал', 'Правый канал'] if channels == 2 else
        [f'Канал {i+1}' for i in range(channels)]
    )
    
    for i in range(channels):
        ax1 = fig.add_subplot(gs[0, i])
        ax1.plot(
            time_original,
            original_audio[:samples_orig, i],
            color=colors[0],
            linewidth=0.7,
            label='Оригинал'
        )
        ax1.set_title(f'{channel_names[i]} - Оригинал', fontsize=12)
        ax1.set_xlabel('Время (секунды)')
        ax1.set_ylabel('Амплитуда')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.set_ylim([-1.1, 1.1])
        
        ax2 = fig.add_subplot(gs[1, i])
        ax2.plot(
            time_sped_up,
            sped_up_audio[:samples_sped, i],
            color=colors[1],
            linewidth=0.7,
            label='Ускоренное'
        )
        ax2.set_title(f'{channel_names[i]} - Ускоренное', fontsize=12)
        ax2.set_xlabel('Время (секунды)')
        ax2.set_ylabel('Амплитуда')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_ylim([-1.1, 1.1])


def _add_info_panel(fig, gs, original_audio, sped_up_audio,
                   original_samplerate, sped_up_samplerate,
                   speed_factor):
    """Добавляет панель с информацией."""
    ax_info = fig.add_subplot(gs[2, :])
    ax_info.axis('off')
    
    original_duration = len(original_audio) / original_samplerate
    sped_up_duration = len(sped_up_audio) / sped_up_samplerate
    
    info_text = (
        f'Информация об аудиофайлах:\n\n'
        f'ОРИГИНАЛЬНОЕ АУДИО:\n'
        f'• Количество сэмплов: {len(original_audio):,}\n'
        f'• Частота дискретизации: {original_samplerate} Hz\n'
        f'• Длительность: {original_duration:.2f} секунд\n'
        f'• Форма массива: {original_audio.shape}\n\n'
        f'УСКОРЕННОЕ АУДИО (x{speed_factor}):\n'
        f'• Количество сэмплов: {len(sped_up_audio):,}\n'
        f'• Частота дискретизации: {sped_up_samplerate} Hz\n'
        f'• Длительность: {sped_up_duration:.2f} секунд\n'
        f'• Форма массива: {sped_up_audio.shape}\n\n'
        f'Скорость увеличена в {speed_factor:.1f} раз\n'
        f'Длительность уменьшена с {original_duration:.2f}с до {sped_up_duration:.2f}с'
    )
    
    ax_info.text(
        0.5,
        0.5,
        info_text,
        transform=ax_info.transAxes,
        fontsize=11,
        verticalalignment='center',
        horizontalalignment='center',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )