import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Time axis
# ----------------------------
T_MIN, T_MAX, N = -4.0, 4.0, 4001


def x_of_t(t: np.ndarray) -> np.ndarray:
    """
    Base signal x(t): sinusoidal signal
    """
    return (
        np.sin(2 * np.pi * 0.5 * t)
        + 0.5 * np.sin(2 * np.pi * 1.5 * t)
    )


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def interpolate_signal(
    t_original: np.ndarray,
    x_original: np.ndarray,
    t_query: np.ndarray
) -> np.ndarray:
    """
    Interpolate using average of two neighboring samples.

    For each t_query, find the nearest original sample to the left and
    to the right, and take their average. If a query time lies exactly
    on an original sample, left == right, so this reduces to that
    sample's value. Queries outside [t_original[0], t_original[-1]]
    are marked as NaN so they can be ignored downstream.
    """
    dt = t_original[1] - t_original[0]
    n_samples = len(t_original)

    # Fractional index of each query point on the original (uniform) grid
    idx = (t_query - t_original[0]) / dt

    left_idx = np.floor(idx).astype(int)
    right_idx = np.ceil(idx).astype(int)

    # Which queries actually fall inside the original time range
    valid = (t_query >= t_original[0]) & (t_query <= t_original[-1])

    # Clip indices so out-of-range lookups don't crash (their result
    # gets discarded via the `valid` mask anyway)
    left_idx = np.clip(left_idx, 0, n_samples - 1)
    right_idx = np.clip(right_idx, 0, n_samples - 1)

    averaged = 0.5 * (x_original[left_idx] + x_original[right_idx])

    return np.where(valid, averaged, np.nan)


def time_scale(
    t: np.ndarray,
    x: np.ndarray,
    k: int
) -> np.ndarray:
    """
    Time sub-scaling:
        y(t) = x(t / k)
    """
    t_query = t / k
    return interpolate_signal(t, x, t_query)


def plot_pair(t: np.ndarray, x: np.ndarray, y: np.ndarray, title: str):
    """
    Plot graphs.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(t, x, label='x(t)')
    plt.plot(t, y, label='y(t)')
    plt.title(title)
    plt.xlabel('t')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)


# ----------------------------
# Main
# ----------------------------
def main():
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_of_t(t)

    k = 2   # sub-scaling factor
    y = time_scale(t, x, k)

    plot_pair(
        t,
        x,
        y,
        title=f"Time Sub-scaling: y(t) = x(t / {k})"
    )
    plt.savefig('time_subscaling.png')
    # plt.show()


if __name__ == "__main__":
    main()