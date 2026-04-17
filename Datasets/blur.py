import cv2
import numpy as np
import os
import argparse
import random
from tqdm import tqdm

# Creates filter that offsets pixels by size at specified angle
def motion_blur_kernel(size, angle):
    kernel = np.zeros((size, size), dtype=np.float32)
    center = size // 2

    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    for i in range(size):
        x = int(center + (i - center) * cos_a)
        y = int(center + (i - center) * sin_a)

        if 0 <= x < size and 0 <= y < size:
            kernel[y, x] = 1.0

    if np.sum(kernel) == 0:
        kernel[center, center] = 1.0

    return kernel / np.sum(kernel)

# Uses opencv and filter to apply motion blur
def apply_motion_blur(img, size, angle):
    kernel = motion_blur_kernel(size, angle)
    return cv2.filter2D(img, -1, kernel)

# Uses opencv to apply generic gaussian blur
def apply_gaussian_blur(img, sigma):
    ksize = int(6 * sigma + 1)
    if ksize % 2 == 0:
        ksize += 1 # enforce odd for blur math
    return cv2.GaussianBlur(img, (ksize, ksize), sigma)

# Updates every image (png or jpg) in folder with specified blur
def process_folder(folder, motion_strength, gaussian_sigma, random_angle):
    images = sorted([
        f for f in os.listdir(folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    for name in tqdm(images):
        path = os.path.join(folder, name)
        img = cv2.imread(path)

        if img is None:
            continue

        # Apply motion blur first (if enabled)
        if motion_strength is not None:
            size = max(3, int(motion_strength))
            if size % 2 == 0:
                size += 1 # enforce odd for blur math

            angle = random.uniform(0, np.pi) if random_angle else 0.0
            img = apply_motion_blur(img, size, angle)

        # Then Gaussian blur (if enabled)
        if gaussian_sigma is not None:
            img = apply_gaussian_blur(img, gaussian_sigma)

        # Only write if at least one transform was applied
        if motion_strength is None and gaussian_sigma is None:
            continue

        cv2.imwrite(path, img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--folder", required=True)

    # Optional blurs (must enable)
    parser.add_argument("--motion", type=float, default=None,
                        help="Motion blur kernel size (odd int after conversion)")

    parser.add_argument("--gaussian", type=float, default=None,
                        help="Gaussian sigma")

    parser.add_argument("--random_angle", action="store_true")

    args = parser.parse_args()

    process_folder(
        args.folder,
        args.motion,
        args.gaussian,
        args.random_angle
    )
