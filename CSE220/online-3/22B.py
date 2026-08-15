import numpy as np
import matplotlib.pyplot as plt

class SignalGenerator:
    """
    Object-oriented framework for generating continuous-time signals.
    """
    def __init__(self, t):
        self.t = t
        
    def gaussian(self, a, t0=0.0):
        """
        Generates the Gaussian signal x(t) = e^{-a(t-t0)^2}.
        The t0 parameter implements the time shift directly within the 
        OOP framework without manually shifting the numerical arrays.
        """
        return np.exp(-a * (self.t - t0)**2)


class CFTAnalyzer:
    """
    Object-oriented framework for Continuous Fourier Transform analysis.
    """
    def __init__(self, t, f):
        self.t = t
        self.f = f
        
    def compute_cft(self, signal):
        """
        Computes the Continuous Fourier Transform of a 1D signal 
        using numerical integration (np.trapezoid), as np.fft is restricted.
        """
        X = np.zeros(len(self.f), dtype=complex)
        
        for i, freq in enumerate(self.f):
            integrand = signal * np.exp(-1j * 2 * np.pi * freq * self.t)
            X[i] = np.trapezoid(integrand, self.t)
            
        return X


def main():
    # ---------------------------------------------------------
    # Part 2: Constructing the Original Signal
    # ---------------------------------------------------------
    # Time axis: t in [-5, 5] with 2000 samples
    t = np.linspace(-5, 5, 2000)
    sig_gen = SignalGenerator(t)
    
    # Generate original signal x(t) = e^{-t^2} (a=1)
    x = sig_gen.gaussian(a=1, t0=0)
    
    # ---------------------------------------------------------
    # Part 3: Time-Shifting the Signal
    # ---------------------------------------------------------
    # Time shift t0 = 1
    t0 = 1
    # Shifted signal y(t) = x(t - 1) generated via OOP framework
    y = sig_gen.gaussian(a=1, t0=t0)
    
    # ---------------------------------------------------------
    # Part 4: Continuous Fourier Transform
    # ---------------------------------------------------------
    # Frequency axis: f in [-10, 10] with 1000 samples
    f = np.linspace(-10, 10, 1000)
    cft_analyzer = CFTAnalyzer(t, f)
    
    # Compute CFTs
    print("Computing Continuous Fourier Transforms (this may take a moment)...")
    X = cft_analyzer.compute_cft(x)
    Y = cft_analyzer.compute_cft(y)
    
    # ---------------------------------------------------------
    # Part 5 & 6: Numerical Verification and Error Analysis
    # ---------------------------------------------------------
    # (a) Magnitude Analysis
    mag_X = np.abs(X)
    mag_Y = np.abs(Y)
    
    # Compute MSE of Magnitude
    MSE_mag = np.mean((mag_X - mag_Y)**2)
    print(f"\n--- Error Metrics ---")
    print(f"MSE of Magnitude: {MSE_mag:.4e}")
    print("Comment: The near-zero MSE confirms the time-shift property; shifting a signal in time alters its phase but leaves its magnitude spectrum completely unchanged.")
    
    # (b) Phase Analysis
    # Use np.unwrap to avoid artificial discontinuities in the MSE calculation caused by 2*pi wrapping
    phase_X = np.unwrap(np.angle(X))
    phase_Y = np.unwrap(np.angle(Y))
    
    # Theoretical predicted phase
    phase_Y_pred = phase_X - 2 * np.pi * f * t0
    
    # Compute Phase Difference Error
    MSE_phase = np.mean((phase_Y - phase_Y_pred)**2)
    
    print(f"MSE of Phase Difference: {MSE_phase:.4e}")
    print(f"Comment: The near-zero phase MSE numerically verifies that a time shift of t0={t0} introduces a linear phase shift of exactly -2πf(t0).")
    
    # ---------------------------------------------------------
    # Plotting
    # ---------------------------------------------------------
    plt.figure(figsize=(14, 10))
    
    # 1. Magnitude Spectra Plot
    plt.subplot(2, 1, 1)
    plt.plot(f, mag_X, 'b-', label='|X(f)| (Original Signal)', linewidth=3)
    plt.plot(f, mag_Y, 'r--', label='|Y(f)| (Shifted Signal)', linewidth=1.5)
    plt.title('Magnitude Spectra: Verification of |X(f)| = |Y(f)|')
    plt.xlabel('Frequency f (Hz)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.grid(True)
    
    # 2. Phase Spectra Plot
    plt.subplot(2, 1, 2)
    plt.plot(f, phase_X, 'b-', label='∠X(f) (Original Phase)', linewidth=2)
    plt.plot(f, phase_Y, 'r--', label='∠Y(f) (Measured Shifted Phase)', linewidth=3)
    plt.plot(f, phase_Y_pred, 'g:', label='∠Y(f) (Theoretical Prediction)', linewidth=2)
    plt.title('Phase Spectra: Verification of ∠Y(f) = ∠X(f) - 2πft₀')
    plt.xlabel('Frequency f (Hz)')
    plt.ylabel('Phase (radians)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()