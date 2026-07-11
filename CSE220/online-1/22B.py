import numpy as np
import matplotlib.pyplot as plt


def sinusoid(n: np.ndarray, A: float, Omega0: float, phi: float) -> np.ndarray:
    # x[n] = A cos(Omega0 * n + phi)
    return A * np.cos(Omega0 * n + phi)


def time_shift_sinusoid(n: np.ndarray, A: float, Omega0: float, phi: float, n0: int) -> np.ndarray:
    # x[n - n0] = A cos(Omega0 * (n - n0) + phi)
    return A * np.cos(Omega0 * (n - n0) + phi)


def phase_change_sinusoid(n: np.ndarray, A: float, Omega0: float, phi: float, phi0: float) -> np.ndarray:
    # Same sinusoid, but with an extra phase offset phi0 added to the original phase
    return A * np.cos(Omega0 * n + phi + phi0)


# -----------------------------
# 2) Utility functions
# -----------------------------
def mse(a: np.ndarray, b: np.ndarray) -> float:
    """Mean squared error between two sequences of equal length."""
    return float(np.mean((a - b) ** 2))


def stem_plot(ax, n, x, label):
    """A nicer stem plot for discrete-time sequences."""
    markerline, stemlines, baseline = ax.stem(n, x, label=label)
    baseline.set_visible(False)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("n")
    ax.set_ylabel("Amplitude")


# -----------------------------
# 3) Main experiment
# -----------------------------
def main():
    # Base sinusoid parameters (you may change these to experiment)
    A = 1.0
    Omega0 = np.pi / 4
    phi = 0.0

    # Index range
    n = np.arange(-20, 21)  # -20, -19, ..., 20

    # Original signal
    x = sinusoid(n, A, Omega0, phi)

    # ---------------------------------------------------------------
    # Part A: does a time shift correspond to SOME phase change?
    # ---------------------------------------------------------------
    n0 = 5  # integer time shift
    x_time = time_shift_sinusoid(n, A, Omega0, phi, n0)

    # x[n - n0] = A cos(Omega0*n + (phi - Omega0*n0))
    # so a time shift by n0 is EXACTLY equal to a phase change by:
    phi0_equiv = -Omega0 * n0

    x_phase_equiv = phase_change_sinusoid(n, A, Omega0, phi, phi0_equiv)

    err_A = mse(x_time, x_phase_equiv)
    print("[Part A] MSE between time-shifted and equivalent phase-changed:", err_A)
    print(
        f"[Part A] n0={n0}  ->  exact equivalent phi0 = -Omega0*n0 = {phi0_equiv:.6f} rad\n")

    fig1, ax1 = plt.subplots(figsize=(9, 4))
    stem_plot(ax1, n, x, "original x[n]")
    stem_plot(ax1, n, x_time, f"time shift by n0={n0}")
    stem_plot(ax1, n, x_phase_equiv, f"phase change by phi0={phi0_equiv:.3f}")
    ax1.set_title("Part A: Time shift vs. its exactly-equivalent phase change")
    ax1.legend()
    fig1.tight_layout()
    fig1.savefig("part_A_time_shift_vs_phase.png")

    # ---------------------------------------------------------------
    # Part B: does an ARBITRARY phase change correspond to SOME
    # integer time shift?
    # ---------------------------------------------------------------
    phi0 = 1.0  # an arbitrary phase change (not a multiple of Omega0)
    x_phase = phase_change_sinusoid(n, A, Omega0, phi, phi0)

    # Search over integer shifts to see if any time shift matches this phase change
    k_min, k_max = -12, 12
    best_k = None
    best_err = None

    for k in range(k_min, k_max + 1):
        x_time_k = time_shift_sinusoid(n, A, Omega0, phi, k)
        e = mse(x_time_k, x_phase)
        if (best_err is None) or (e < best_err):
            best_err = e
            best_k = k

    print(
        f"[Part B] Best matching integer shift in [{k_min},{k_max}] is k={best_k} with MSE={best_err}")
    print("[Part B] MSE is NOT zero: an arbitrary phase change generally has no exact")
    print("         integer-sample time-shift equivalent, since that would require")
    print(
        f"         phi0 = -Omega0*k for some integer k (i.e. phi0 must be a multiple")
    print(
        f"         of Omega0 = {Omega0:.6f}). Our phi0={phi0} is not such a multiple.\n")

    x_time_best = time_shift_sinusoid(n, A, Omega0, phi, best_k)

    fig2, ax2 = plt.subplots(figsize=(9, 4))
    stem_plot(ax2, n, x_phase, f"phase change by phi0={phi0:.3f}")
    stem_plot(ax2, n, x_time_best, f"best time shift k={best_k}")
    ax2.set_title(
        "Part B: Arbitrary phase change vs. best-matching integer time shift")
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig("part_B_phase_vs_best_time_shift.png")

    # plt.show()


if __name__ == "__main__":
    main()
