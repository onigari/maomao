import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

INF = 8


def plot(
    signal,
    title=None,
    y_range=(-1, 3),
    figsize=(8, 3),
    x_label='n (Time Index)',
    y_label='x[n]',
    saveTo=None
):
    plt.figure(figsize=figsize)
    plt.xticks(np.arange(-INF, INF + 1, 1))

    y_range = (y_range[0], max(np.max(signal), y_range[1]) + 1)
    # set y range of
    plt.ylim(*y_range)
    plt.stem(np.arange(-INF, INF + 1, 1), signal)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    if saveTo is not None:
        plt.savefig(saveTo)
    # plt.show()


def init_signal():
    return np.zeros(2 * INF + 1)


def time_scale_signal(x: np.ndarray, k: int) -> np.ndarray:
    # Returns y[n] = x[n/k]. Only defined (nonzero) where n is a multiple of k;
    # all intermediate samples are set to 0.
    n = np.arange(-INF, INF + 1)
    y = np.zeros_like(x)

    mask = (n % k == 0)               # n values that are exact multiples of k
    m = (n[mask] // k).astype(int)    # corresponding original index m = n/k
    valid = (m >= -INF) & (m <= INF)  # keep only m within the stored range

    idx_n = n[mask][valid] + INF      # array positions for those n
    idx_m = m[valid] + INF            # array positions for those m

    y[idx_n] = x[idx_m]
    return y


def time_scale_signal_interpolate(x: np.ndarray, k: int) -> np.ndarray:
    # Same as time_scale_signal, but intermediate samples are filled with the
    # average of the two flanking exact samples (the ones at the nearest
    # multiples of k below and above), instead of 0. A neighbor that falls
    # outside the stored [-INF, INF] range is treated as 0.
    n = np.arange(-INF, INF + 1)
    y = time_scale_signal(x, k)

    lower_n = (np.floor(n / k) * k).astype(int)
    upper_n = lower_n + k

    def gather(idx):
        out = np.zeros_like(x)
        valid = (idx >= -INF) & (idx <= INF)
        out[valid] = y[idx[valid] + INF]
        return out

    lower_val = gather(lower_n)
    upper_val = gather(upper_n)
    interpolated = (lower_val + upper_val) / 2

    exact_mask = (n % k == 0)
    return np.where(exact_mask, y, interpolated)


def main():
    img_root = '.'
    signal = init_signal()
    signal[INF] = 1
    signal[INF+1] = .5
    signal[INF-1] = 2
    signal[INF + 2] = 1
    signal[INF - 2] = .5

    plot(signal, title='Original Signal(x[n])', saveTo=f'{img_root}/x[n].png')
    plot(time_scale_signal(signal, 3),
         title='x[n/3]', saveTo=f'{img_root}/x[n divided by 3].png')
    plot(time_scale_signal(signal, 1),
         title='x[n/1]', saveTo=f'{img_root}/x[n divided by 1].png')
    plot(time_scale_signal_interpolate(signal, 3),
         title='x[n/3] with interpolation', saveTo=f'{img_root}/x[n divided by 3]_with_interpolation.png')
    plot(time_scale_signal_interpolate(signal, 1),
         title='x[n/1] with interpolation', saveTo=f'{img_root}/x[n divided by 1]_with_interpolation.png')


main()
