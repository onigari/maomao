import os
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. ContinuousSignal
# --------------------------------------------------------------------------
class ContinuousSignal:
    """
    Represents a continuous-time signal x(t) defined by a Python function.

    func must accept a numpy array of time samples and return a numpy array
    of the same shape with the corresponding signal values.
    """

    def __init__(self, func):
        self.func = func

    def shift(self, shift):
        """Return a new ContinuousSignal representing x(t - shift)."""
        old_func = self.func
        return ContinuousSignal(lambda t, s=shift, f=old_func: f(t - s))

    def add(self, other):
        """Return a new ContinuousSignal representing x(t) + y(t)."""
        f1, f2 = self.func, other.func
        return ContinuousSignal(lambda t: f1(t) + f2(t))

    def multiply(self, other):
        """Return a new ContinuousSignal representing x(t) * y(t)."""
        f1, f2 = self.func, other.func
        return ContinuousSignal(lambda t: f1(t) * f2(t))

    def multiply_const_factor(self, scaler):
        """Return a new ContinuousSignal representing a * x(t)."""
        f = self.func
        return ContinuousSignal(lambda t, a=scaler, f=f: a * f(t))

    def plot(self, t_min, t_max, num_points=1000, title="Continuous Signal",
             ax=None, label=None, **plot_kwargs):
        """Plot the signal over [t_min, t_max]. If ax is given, plot on it."""
        t = np.linspace(t_min, t_max, num_points)
        y = self.func(t)

        created_fig = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 4))
            created_fig = True

        ax.plot(t, y, label=label, **plot_kwargs)
        ax.set_xlabel("t (Time)")
        ax.set_ylabel("x(t)")
        ax.set_title(title)
        ax.grid(True)
        if label is not None:
            ax.legend()

        if created_fig:
            return fig, ax
        return ax


# --------------------------------------------------------------------------
# 2. LTI_Continuous
# --------------------------------------------------------------------------
class LTI_Continuous:
    """
    Represents a continuous-time LTI system defined by its impulse response
    h(t) (an instance of ContinuousSignal).
    """

    def __init__(self, impulse_response):
        self.impulse_response = impulse_response

    @staticmethod
    def _unit_rect_impulse(delta):
        """
        Base rectangular impulse:
            delta_d(t) = 1/delta   for 0 <= t < delta
                       = 0         otherwise
        """
        def func(t, d=delta):
            return np.where((t >= 0) & (t < d), 1.0 / d, 0.0)
        return ContinuousSignal(func)

    def linear_combination_of_impulses(self, input_signal, delta,
                                        t_min=-3, t_max=3):
        """
        Decomposes input_signal x(t) into a linear combination of shifted
        rectangular impulses of width `delta` and height 1/delta, over the
        window [t_min, t_max).

            t_k = k * delta
            c_k = x(t_k) * delta
            impulse_k(t) = delta_delta(t - t_k)

        Returns:
            impulses : list of ContinuousSignal, one per t_k
            coeffs   : list of float, the corresponding c_k
        """
        base_impulse = self._unit_rect_impulse(delta)

        t_ks = np.arange(t_min, t_max, delta)

        impulses = []
        coeffs = []
        for tk in t_ks:
            x_tk = float(input_signal.func(np.array([tk]))[0])
            c_k = x_tk * delta
            impulse_k = base_impulse.shift(tk)
            impulses.append(impulse_k)
            coeffs.append(c_k)

        return impulses, coeffs

    def output_approx(self, input_signal, delta):
        """
        Not required in this practice (output computation via convolution
        sum). Kept as a stub for a future assignment.
        """
        raise NotImplementedError(
            "output_approx is not implemented in this practice."
        )


# --------------------------------------------------------------------------
# Helper: reconstruct x_hat(t) from impulses/coeffs
# --------------------------------------------------------------------------
def reconstruct_signal(impulses, coeffs):
    """
    Given the impulses and coefficients returned by
    linear_combination_of_impulses, build:
        x_k(t) = c_k * impulse_k(t)
        x_hat(t) = sum_k x_k(t)
    Returns (component_signals, reconstructed_signal)
    """
    components = [imp.multiply_const_factor(c) for imp, c in zip(impulses, coeffs)]

    zero_signal = ContinuousSignal(lambda t: np.zeros_like(t, dtype=float))
    reconstructed = zero_signal
    for comp in components:
        reconstructed = reconstructed.add(comp)

    return components, reconstructed


# --------------------------------------------------------------------------
# 4. main()
# --------------------------------------------------------------------------
def main():
    out_dir = "continuous_practice"
    os.makedirs(out_dir, exist_ok=True)

    # ---------------- Step 1: define system and input signal ----------------
    T1 = 3

    # x(t) = e^{-t} u(t)
    x_signal = ContinuousSignal(lambda t: np.where(t >= 0, np.exp(-t), 0.0))

    # h(t) = u(t)  (built into the system, not used for output here)
    h_signal = ContinuousSignal(lambda t: np.where(t >= 0, 1.0, 0.0))

    system = LTI_Continuous(h_signal)

    # ---------------- Figure 1: Input Signal ----------------
    fig1, ax1 = x_signal.plot(-T1, T1, 1000, title=f"x(t), INF = {T1}")
    fig1.tight_layout()
    fig1.savefig(os.path.join(out_dir, "figure1_input_signal.png"), dpi=150)
    plt.close(fig1)

    # ---------------- Step 2: decompose x(t) into impulses ----------------
    delta = 1
    T2 = 6
    impulses, coeffs = system.linear_combination_of_impulses(
        x_signal, delta, t_min=-T2, t_max=T2
    )
    components, reconstructed = reconstruct_signal(impulses, coeffs)

    # ---------------- Figure 2: components + reconstruction ----------------
    n_components = len(components)
    n_slots = n_components + 1          # +1 for the reconstructed signal
    n_cols = 3
    n_rows = int(np.ceil(n_slots / n_cols))

    fig2, axes2 = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 3 * n_rows))
    axes2 = np.array(axes2).reshape(-1)
    fig2.suptitle("Impulses multiplied by coefficients", fontsize=14)

    t_ks = np.arange(-T2, T2, delta)
    for i, (comp, ck, tk) in enumerate(zip(components, coeffs, t_ks)):
        ax = axes2[i]
        comp.plot(-T2, T2, 500, title=f"delta(t-({tk})) x ({tk:.1f})", ax=ax)
        ax.set_ylim(-0.1, 1.1)

    # reconstructed signal in the next available subplot
    recon_ax = axes2[n_components]
    reconstructed.plot(-T2, T2, 1000, title="Reconstructed Signal", ax=recon_ax)
    recon_ax.set_ylim(-0.1, 1.1)

    # hide any unused subplots
    for j in range(n_slots, len(axes2)):
        axes2[j].axis("off")

    fig2.tight_layout(rect=[0, 0, 1, 0.96])
    fig2.savefig(os.path.join(out_dir, "figure2_components_and_reconstruction.png"), dpi=150)
    plt.close(fig2)

    # ---------------- Figure 3: reconstruction with varying delta ----------------
    deltas = [0.5, 0.1, 0.05, 0.01]
    fig3, axes3 = plt.subplots(2, 2, figsize=(10, 8))
    axes3 = axes3.reshape(-1)

    for ax, d in zip(axes3, deltas):
        imp_d, coeffs_d = system.linear_combination_of_impulses(
            x_signal, d, t_min=-T1, t_max=T1
        )
        _, recon_d = reconstruct_signal(imp_d, coeffs_d)

        recon_d.plot(-T1, T1, 1000, title=f"delta = {d}", ax=ax, label="Reconstructed")
        x_signal.plot(-T1, T1, 1000, title=f"delta = {d}", ax=ax, label="x(t)")

    fig3.suptitle("Reconstruction of input signal with varying delta", fontsize=14)
    fig3.tight_layout(rect=[0, 0, 1, 0.96])
    fig3.savefig(os.path.join(out_dir, "figure3_varying_delta.png"), dpi=150)
    plt.close(fig3)

    print(f"All figures saved in '{out_dir}/'")


if __name__ == "__main__":
    main()
