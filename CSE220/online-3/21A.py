import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapz

# Load and preprocess the image
image = plt.imread('noisy_image.png')  # Replace with your image file path
# show the image
plt.figure()
plt.title('Original Image')
plt.imshow(image, cmap='gray')
plt.show()

if image.ndim == 3:
    # If the image has 4 channels (RGBA), slice to RGB first
    if image.shape[2] == 4:
        image = image[:, :, :3]
    image = np.mean(image, axis=2)  # Convert to grayscale

# Normalize to range [0, 1]. Only divide by 255 if image hasn't already been normalized by imread.
if np.max(image) > 1.0:
    image = image / 255.0

print(image.shape)

sample_rate = 1000

# ==========================================================
# Fourier Transform Operations
# ==========================================================
rows, cols = image.shape
t = np.arange(cols) / sample_rate

# Create orthogonal frequency bins to avoid information loss
if cols % 2 == 0:
    f = np.arange(-cols/2, cols/2) * (sample_rate / cols)
else:
    f = np.arange(-(cols-1)/2, (cols-1)/2 + 1) * (sample_rate / cols)

print("Applying FT row by row...")
F_matrix = np.zeros((rows, len(f)), dtype=complex)
for i in range(rows):
    # Vectorized FT across all frequencies for the current row
    integrand = image[i, :] * np.exp(-1j * 2 * np.pi * f[:, None] * t)
    F_matrix[i, :] = trapz(integrand, t, axis=1)

# Detect the sinusoidal noise frequency (vertical bands)
avg_mag = np.mean(np.abs(F_matrix), axis=0)

# Mask the DC component (at f=0) to accurately locate the noise spikes
dc_mask = np.abs(f) < (sample_rate / cols) * 2
avg_mag_no_dc = avg_mag.copy()
avg_mag_no_dc[dc_mask] = 0

# Set a threshold to pick out dominant non-DC frequencies (the noise)
threshold = np.max(avg_mag_no_dc) * 0.5
noise_indices = np.where(avg_mag_no_dc > threshold)[0]
print(f"Filtering out noise frequencies at indices: {noise_indices}")

# Zero out the detected noise peaks (with a small window buffer)
for idx in noise_indices:
    window = 2
    F_matrix[:, max(0, idx-window):min(len(f), idx+window+1)] = 0

# ==========================================================
# Inverse Fourier Transform Operations
# ==========================================================
print("Reconstructing denoised image using Inverse FT...")
denoised_image = np.zeros((rows, cols))
for i in range(rows):
    # Vectorized Inverse FT across time for the current row
    integrand = F_matrix[i, :] * np.exp(1j * 2 * np.pi * t[:, None] * f)
    denoised_image[i, :] = np.real(trapz(integrand, f, axis=1))

# Normalize the final reconstructed image back to [0, 1] for saving and display
denoised_image = (denoised_image - np.min(denoised_image)) / \
    (np.max(denoised_image) - np.min(denoised_image))

plt.imsave('denoised_image.png', denoised_image, cmap='gray')

plt.figure()
plt.title('Denoised Image')
plt.imshow(denoised_image, cmap='gray')
plt.show()
