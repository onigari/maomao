import numpy as np
import matplotlib.pyplot as plt

def compute_cft(signal, t, f):
    """
    Computes the Continuous Fourier Transform of a 1D signal manually 
    using numerical integration (np.trapezoid), as np.fft is not allowed.
    """
    # Initialize output array
    X = np.zeros(len(f), dtype=complex)
    
    # Compute the integral for each frequency
    for i, freq in enumerate(f):
        integrand = signal * np.exp(-1j * 2 * np.pi * freq * t)
        X[i] = np.trapezoid(integrand, t)
        
    return X

def phase_mse(cft_prop, cft_dir, magnitude_threshold=0.5):
    """
    Calculates Phase MSE. Phase is practically random noise where the 
    signal magnitude is near zero. To get a meaningful MSE, we only 
    compare the phase where the magnitude is significant.
    """
    # Find indices where the magnitude is significant (ignoring noise)
    valid_idx = np.abs(cft_dir) > magnitude_threshold
    
    if not np.any(valid_idx):
        return 0.0
        
    # Calculate phase difference
    phase_prop = np.angle(cft_prop[valid_idx])
    phase_dir = np.angle(cft_dir[valid_idx])
    
    # Wrap phase difference to [-pi, pi]
    diff = (phase_prop - phase_dir + np.pi) % (2 * np.pi) - np.pi
    return np.mean(diff**2)

def main():
    # ---------------------------------------------------------
    # 1. Define Time and Frequency Domains
    # ---------------------------------------------------------
    t = np.linspace(-10, 10, 2000)
    # The frequencies in the signal are f1 = 4/(2*pi) ≈ 0.636 Hz, f2 = 6/(2*pi) ≈ 0.955 Hz
    f = np.linspace(-2, 2, 500)
    
    # ---------------------------------------------------------
    # 2. Define Original Signal and its Derivatives
    # ---------------------------------------------------------
    # x(t) = 0.5*cos(4t) + 0.5*sin(6t)
    x = 0.5 * np.cos(4 * t) + 0.5 * np.sin(6 * t)
    
    # 1st Derivative: x'(t) = -2*sin(4t) + 3*cos(6t)
    y1 = -2 * np.sin(4 * t) + 3 * np.cos(6 * t)
    
    # 2nd Derivative: x''(t) = -8*cos(4t) - 18*sin(6t)
    y2 = -8 * np.cos(4 * t) - 18 * np.sin(6 * t)
    
    # 3rd Derivative: x'''(t) = 32*sin(4t) - 108*cos(6t)
    y3 = 32 * np.sin(4 * t) - 108 * np.cos(6 * t)
    
    # ---------------------------------------------------------
    # 3. Compute CFTs Directly
    # ---------------------------------------------------------
    print("Computing Direct CFTs...")
    X = compute_cft(x, t, f)
    Y1_dir = compute_cft(y1, t, f)
    Y2_dir = compute_cft(y2, t, f)
    Y3_dir = compute_cft(y3, t, f)
    
    # ---------------------------------------------------------
    # 4. Compute CFTs via Derivative Property
    # ---------------------------------------------------------
    j2pif = 1j * 2 * np.pi * f
    
    Y1_prop = j2pif * X
    Y2_prop = (j2pif ** 2) * X
    Y3_prop = (j2pif ** 3) * X
    
    # ---------------------------------------------------------
    # 5. MSE Analysis
    # ---------------------------------------------------------
    # MSE for 1st Derivative
    mse_mag_1 = np.mean((np.abs(Y1_prop) - np.abs(Y1_dir))**2)
    mse_ph_1 = phase_mse(Y1_prop, Y1_dir)
    
    # MSE for 2nd Derivative
    mse_mag_2 = np.mean((np.abs(Y2_prop) - np.abs(Y2_dir))**2)
    mse_ph_2 = phase_mse(Y2_prop, Y2_dir)
    
    # MSE for 3rd Derivative
    mse_mag_3 = np.mean((np.abs(Y3_prop) - np.abs(Y3_dir))**2)
    mse_ph_3 = phase_mse(Y3_prop, Y3_dir)
    
    print("\n--- Mean Squared Error (MSE) Analysis ---")
    print(f"1st Derivative -> Magnitude MSE: {mse_mag_1:.2e}, Phase MSE (thresholded): {mse_ph_1:.2e}")
    print(f"2nd Derivative -> Magnitude MSE: {mse_mag_2:.2e}, Phase MSE (thresholded): {mse_ph_2:.2e}")
    print(f"3rd Derivative -> Magnitude MSE: {mse_mag_3:.2e}, Phase MSE (thresholded): {mse_ph_3:.2e}")
    
    # ---------------------------------------------------------
    # 6. Plotting & Verification
    # ---------------------------------------------------------
    derivatives = [
        ("1st Derivative", Y1_prop, Y1_dir),
        ("2nd Derivative", Y2_prop, Y2_dir),
        ("3rd Derivative", Y3_prop, Y3_dir)
    ]
    
    plt.figure(figsize=(15, 12))
    
    for i, (title, Y_prop, Y_dir) in enumerate(derivatives):
        # Plot Magnitude
        plt.subplot(3, 2, 2*i + 1)
        plt.plot(f, np.abs(Y_prop), 'b-', label='Property: |(j2πf)^n X(f)|', linewidth=3)
        plt.plot(f, np.abs(Y_dir), 'r--', label='Direct: |CFT{yn(t)}|', linewidth=1.5)
        plt.title(f'{title} - Magnitude')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.grid(True)
        
        # Plot Phase
        plt.subplot(3, 2, 2*i + 2)
        # Only plot phase where the magnitude is significant to avoid visual noise
        valid = np.abs(Y_dir) > 0.5
        
        # Plotting scatter instead of line due to discontinuous phase valid zones
        plt.scatter(f[valid], np.angle(Y_prop[valid]), color='b', label='Property Phase', marker='o', s=40)
        plt.scatter(f[valid], np.angle(Y_dir[valid]), color='r', label='Direct Phase', marker='x', s=20)
        plt.title(f'{title} - Phase (at peaks)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Phase (radians)')
        plt.legend()
        plt.grid(True)
        
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()