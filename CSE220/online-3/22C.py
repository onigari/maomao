import numpy as np
import matplotlib.pyplot as plt

class SignalGenerator:
    """
    Object-oriented framework for generating continuous-time signals 
    and applying specific transformations.
    """
    def __init__(self, t):
        self.t = t
        
    def square(self, t_val):
        """Standard rectangular pulse (Square) centered at 0 with width 1."""
        return np.where(np.abs(t_val) <= 0.5, 1.0, 0.0)
        
    def triangle(self, t_val):
        """Standard triangular pulse centered at 0 with base width 2."""
        return np.where(np.abs(t_val) <= 1.0, 1.0 - np.abs(t_val), 0.0)
        
    def generate_x(self):
        """Generates original signal x(t) = Square(t) + Triangle(t)."""
        return self.square(self.t) + self.triangle(self.t)
        
    def generate_y(self, a, f0):
        """
        Generates modified signal y(t).
        Applies time compression by 'a' and a phase (frequency) shift by 2*pi*f0*t.
        """
        # Time compression: scale time axis by a
        t_scaled = a * self.t
        x_scaled = self.square(t_scaled) + self.triangle(t_scaled)
        
        # Phase shifting (Frequency shifting): multiply by exp(j*2*pi*f0*t)
        phase_shift = np.exp(1j * 2 * np.pi * f0 * self.t)
        
        return x_scaled * phase_shift


class CFTAnalyzer:
    """
    Object-oriented framework for Continuous Fourier Transform (CFT) analysis.
    """
    def __init__(self, t, f):
        self.t = t
        self.f = f
        
    def compute_cft(self, signal, custom_freqs=None):
        """
        Computes the CFT of a 1D signal using numerical integration 
        (np.trapezoid). Capable of evaluating on a custom frequency grid 
        to help verify scaling/shifting properties.
        """
        freqs_to_use = self.f if custom_freqs is None else custom_freqs
        X = np.zeros(len(freqs_to_use), dtype=complex)
        
        for i, freq in enumerate(freqs_to_use):
            integrand = signal * np.exp(-1j * 2 * np.pi * freq * self.t)
            X[i] = np.trapezoid(integrand, self.t)
            
        return X


def main():
    # ---------------------------------------------------------
    # 1. Initialization and Signal Generation
    # ---------------------------------------------------------
    # Time axis: t in [-5, 5] with 2000 samples
    t = np.linspace(-5, 5, 2000)
    # Frequency axis: f in [-10, 10] with 1000 samples
    f = np.linspace(-10, 10, 1000)
    
    # Parameters given in the prompt
    f0 = 10
    a = 10
    
    sig_gen = SignalGenerator(t)
    cft_analyzer = CFTAnalyzer(t, f)
    
    # Generate signals
    x = sig_gen.generate_x()
    y = sig_gen.generate_y(a=a, f0=f0)
    
    # ---------------------------------------------------------
    # 2. Compute CFTs
    # ---------------------------------------------------------
    print("Computing CFTs (Numerical Integration)...")
    
    # CFT of y(t) evaluated at f
    Y = cft_analyzer.compute_cft(y)
    
    # CFT of x(t) evaluated at transformed frequency (f - f0)/a
    transformed_f = (f - f0) / a
    X_transformed = cft_analyzer.compute_cft(x, custom_freqs=transformed_f)
    
    # Compute the theoretical prediction based on the scaling/shifting properties
    Y_theoretical = (1 / np.abs(a)) * X_transformed
    
    # ---------------------------------------------------------
    # 3. Verify Properties & Compute MSE
    # ---------------------------------------------------------
    mag_Y = np.abs(Y)
    mag_Y_theoretical = np.abs(Y_theoretical)
    
    phase_Y = np.angle(Y)
    phase_X_transformed = np.angle(X_transformed)
    
    # Error Analysis
    MSE_magnitude = np.mean((mag_Y - mag_Y_theoretical)**2)
    
    # Phase Difference Error (Accounting for numerical noise at near-zero magnitudes)
    # We apply np.unwrap to avoid arbitrary 2*pi jumps when computing differences
    MSE_phase = np.mean((np.unwrap(phase_Y) - np.unwrap(phase_X_transformed))**2)
    
    print("\n--- Error Analysis ---")
    print(f"MSE of Magnitude: {MSE_magnitude:.4e}")
    print(f"MSE of Phase: {MSE_phase:.4e}")
    
    print("\n--- Effects of Transformations ---")
    print("(i) Phase Shift (Multiplying by e^{j 2π f_0 t}): Shifts the entire spectrum in the frequency domain to be centered at f0.")
    print("(ii) Time Compression (scaling by a): Expands the spectrum in the frequency domain by a factor of 'a' and scales its magnitude down by 1/|a|.")
    
    # ---------------------------------------------------------
    # 4. Plotting & Verification
    # ---------------------------------------------------------
    plt.figure(figsize=(12, 10))
    
    # Magnitude Plot
    plt.subplot(2, 1, 1)
    plt.plot(f, mag_Y, 'b-', label='|Y(f)| (Direct CFT of y(t))', linewidth=3)
    plt.plot(f, mag_Y_theoretical, 'r--', label='1/|a| * |X((f-f0)/a)|', linewidth=1.5)
    plt.title('Magnitude Verification: |Y(f)| = 1/|a| * |X((f-f0)/a)|')
    plt.xlabel('Frequency f (Hz)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.grid(True)
    
    # Phase Plot
    plt.subplot(2, 1, 2)
    plt.plot(f, phase_Y, 'b-', label='∠Y(f)', linewidth=3)
    plt.plot(f, phase_X_transformed, 'r--', label='∠X((f-f0)/a)', linewidth=1.5)
    plt.title('Phase Verification: ∠Y(f) = ∠X((f-f0)/a)')
    plt.xlabel('Frequency f (Hz)')
    plt.ylabel('Phase (Radians)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()