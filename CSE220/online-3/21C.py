import numpy as np
import matplotlib.pyplot as plt

def compute_ft(t, y, f):
    """
    Computes the Continuous Fourier Transform of the signal 
    using numerical integration (np.trapz).
    """
    F = np.zeros(len(f), dtype=complex)
    for i, freq in enumerate(f):
        integrand = y * np.exp(-1j * 2 * np.pi * freq * t)
        F[i] = np.trapz(integrand, t)
    return F

def main():
    # 1. Define time axis (e.g., 2 seconds duration for good resolution)
    t = np.linspace(0, 2, 2000)
    
    # 2. Original Function provided in the prompt
    f_t = 2 * np.sin(14 * np.pi * t) - np.sin(2 * np.pi * t) * (4 * np.sin(2 * np.pi * t) * np.sin(14 * np.pi * t) - 1)
    
    # 3. Frequency axis for FT (0 to 12 Hz is enough to capture our expected peaks)
    f = np.linspace(0, 12, 1200) 
    print("Computing Fourier Transform...")
    F_f = compute_ft(t, f_t, f)
    
    # 4. Find peak frequencies from the FT magnitude spectrum
    mag = np.abs(F_f)
    threshold = np.max(mag) * 0.5  # Set a threshold to ignore noise
    detected_freqs = []
    
    # Simple peak detection logic
    for i in range(1, len(mag)-1):
        if mag[i] > threshold and mag[i] > mag[i-1] and mag[i] > mag[i+1]:
            detected_freqs.append(f[i])
            
    print(f"Detected Frequencies via FT (Hz): {[round(freq, 2) for freq in detected_freqs]}")
    
    # 5. Reconstruct the signal based on findings
    # The prompt states the components have amplitude=1 and phase=0
    reconstructed_f_t = np.zeros_like(t)
    for freq in detected_freqs:
        clean_freq = round(freq) # Round to nearest integer Hz
        reconstructed_f_t += np.sin(2 * np.pi * clean_freq * t)
        
    # 6. Check equality (MSE)
    mse = np.mean((f_t - reconstructed_f_t)**2)
    print(f"Mean Squared Error (Original vs Reconstructed): {mse:.4e}")
    if mse < 1e-4:
        print("Success! The summation of the detected sine waves equals the original function.")

    # 7. Plotting
    plt.figure(figsize=(12, 10))
    
    # Plot FT Magnitude
    plt.subplot(3, 1, 1)
    plt.plot(f, mag, color='purple', linewidth=2)
    plt.title('Fourier Transform Magnitude Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    
    # Plot Original Function
    plt.subplot(3, 1, 2)
    plt.plot(t, f_t, label='Original f(t)', color='blue', linewidth=3)
    plt.title('Original Function')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    
    # Plot Reconstructed Function
    plt.subplot(3, 1, 3)
    plt.plot(t, reconstructed_f_t, label='Reconstructed (Summation of Detected Sines)', color='red', linestyle='--', linewidth=2)
    plt.title('Reconstructed Function from FT Frequencies')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()