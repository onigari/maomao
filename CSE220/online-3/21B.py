import numpy as np
import matplotlib.pyplot as plt

def generate_piecewise_function(t):
    """
    Generates the piecewise function based on the provided graph.
    - Parabola from -3 to -1: (t+3)^2
    - Straight lines from -1 to 1 peaking at 5: 5 - |t|
    - Parabola from 1 to 3: (t-3)^2
    - 0 elsewhere
    """
    y = np.zeros_like(t)
    for i, val in enumerate(t):
        if -3 <= val < -1:
            y[i] = (val + 3)**2
        elif -1 <= val <= 1:
            y[i] = 5 - abs(val)
        elif 1 < val <= 3:
            y[i] = (val - 3)**2
        else:
            y[i] = 0
    return y

def compute_ft(t, y, f):
    """
    Computes the Continuous Fourier Transform of the signal 
    using numerical integration (trapz) as per offline instructions.
    """
    F = np.zeros(len(f), dtype=complex)
    for i, freq in enumerate(f):
        integrand = y * np.exp(-1j * 2 * np.pi * freq * t)
        # Using np.trapz (or np.trapezoid) as strictly required
        F[i] = np.trapz(integrand, t)
    return F

def main():
    # 1. Define time and frequency axes
    t = np.linspace(-10, 10, 2000)
    f = np.linspace(-10, 10, 2000)
    
    # 2. Generate the piecewise signal
    f_t = generate_piecewise_function(t)
    
    # Plotting the original function to verify it matches Figure 1
    plt.figure(figsize=(10, 4))
    plt.plot(t, f_t, label='Piecewise Function', color='dimgray')
    plt.title('Piecewise Function')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.show()

    # 3. Compute Fourier Transform
    print("Computing Fourier Transform...")
    F_f = compute_ft(t, f_t, f)
    
    # 4. Prove Parseval's Theorem
    # Parseval's Theorem: Integral of |f(t)|^2 dt = Integral of |F(f)|^2 df
    print("Calculating energies...")
    energy_time = np.trapz(np.abs(f_t)**2, t)
    energy_freq = np.trapz(np.abs(F_f)**2, f)
    
    print("\n--- Parseval's Theorem Verification ---")
    print(f"Total Energy in Time Domain:      {energy_time:.4f}")
    print(f"Total Energy in Frequency Domain: {energy_freq:.4f}")
    
    # Calculate difference
    difference = abs(energy_time - energy_freq)
    print(f"Absolute Difference:              {difference:.4e}")
    
    if difference < 1e-2:
        print("Parseval's theorem is successfully proven! The energies are approximately equal.")
    else:
        print("Parseval's theorem verification failed. Check bounds or sample rate.")

if __name__ == "__main__":
    main()