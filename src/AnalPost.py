import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, filters, color, exposure, morphology, feature, restoration, measure, transform, util
from skimage.segmentation import slic, mark_boundaries
from skimage.filters import median, rank, gabor, laplace, prewitt, roberts, scharr
from skimage.morphology import disk
from skimage.restoration import denoise_wavelet
from skimage.feature import canny, corner_harris, corner_peaks, local_binary_pattern, graycomatrix, graycoprops
from skimage.measure import moments_hu, find_contours
from skimage.transform import radon, hough_circle, hough_circle_peaks

def combined_image_analysis(image, output_folder):
    image = np.array(image)
    # Open a text file to write the output
    with open(os.path.join(output_folder, 'analysis_output.txt'), 'w') as f:
        # Check if the image has an alpha channel and remove it
        if image.shape[-1] == 4:
            image = image[..., :3]

        gray_image = color.rgb2gray(image)

        # Apply Gaussian filter for smoothing
        smoothed_image = filters.gaussian(gray_image, sigma=1)

        # Apply median filtering
        median_filtered_image = median(smoothed_image, disk(3))

        # Wavelet denoising
        denoised_image = denoise_wavelet(gray_image)

        # Histogram equalization
        equalized_image = exposure.equalize_hist(gray_image)

        # CLAHE
        clahe_image = exposure.equalize_adapthist(gray_image, clip_limit=0.03)

        # Morphological operations: dilation and erosion
        selem = morphology.disk(3)
        dilated = morphology.dilation(median_filtered_image, selem)
        eroded = morphology.erosion(dilated, selem)

        # SLIC segmentation
        segments = slic(image, n_segments=100, compactness=10, sigma=1)
        segmented_image = mark_boundaries(image, segments)

        # Convert image to uint8 for rank filtering
        gray_image_uint8 = util.img_as_ubyte(gray_image)
        rank_filtered_image = rank.mean(gray_image_uint8, selem)

        # Edge detection using Canny
        edges_canny = canny(gray_image, sigma=1)

        # Edge detection using various filters
        edges_sobel = filters.sobel(median_filtered_image)
        edges_laplace = laplace(median_filtered_image)
        edges_prewitt = prewitt(median_filtered_image)
        edges_roberts = roberts(median_filtered_image)
        edges_scharr = scharr(median_filtered_image)

        # Gabor filter for texture
        gabor_filtered, _ = gabor(median_filtered_image, frequency=0.6)

        # Enhance contrast of Gabor-filtered image
        gabor_filtered_enhanced = exposure.rescale_intensity(gabor_filtered, in_range='image', out_range=(0, 1))

        # Contour detection
        contours = find_contours(gray_image, 0.8)

        # Hough transform for circles
        hough_radii = np.arange(15, 30, 2)
        hough_res = hough_circle(edges_canny, hough_radii)
        accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=3)

        # Texture analysis using GLCM
        glcm = graycomatrix((gray_image * 255).astype(np.uint8), distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
        energy = graycoprops(glcm, 'energy')[0, 0]
        homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
        f.write(f"Texture Analysis - Contrast: {contrast}, Dissimilarity: {dissimilarity}, Energy: {energy}, Homogeneity: {homogeneity}\n")

        # Texture analysis using LBP
        lbp = local_binary_pattern((gray_image * 255).astype(np.uint8), P=8, R=1, method='uniform')
        lbp_hist, _ = np.histogram(lbp, bins=np.arange(257), density=True)
        f.write(f"LBP Histogram: {lbp_hist}\n")

        # Region properties analysis
        labels = measure.label(eroded)
        regions = measure.regionprops(labels)
        for region in regions:
            eccentricity = region.eccentricity
            compactness = (region.perimeter ** 2) / region.area if region.area > 0 else 0
            f.write(f"Region: {region.label}, Area: {region.area}, Perimeter: {region.perimeter}, Eccentricity: {eccentricity}, Compactness: {compactness}\n")

        # Corner detection using Harris
        corners = corner_peaks(corner_harris(gray_image), min_distance=5)
        f.write(f"Number of corners detected: {len(corners)}\n")

        # Shape analysis using Hu moments
        hu_moments = moments_hu(gray_image)
        f.write(f"Hu Moments: {hu_moments}\n")

        # Shape analysis using Fourier descriptors
        for contour in contours:
            fourier_result = np.fft.fft(contour)
            f.write(f"Fourier Descriptors: {fourier_result[:5]}\n")  # Display first 5 descriptors

        # Hough transform for lines
        hough_lines = transform.probabilistic_hough_line(edges_canny, threshold=10, line_length=5, line_gap=3)
        f.write(f"Number of lines detected: {len(hough_lines)}\n")

        # Radon transform
        padded_image = np.pad(gray_image, ((gray_image.shape[0]//2, gray_image.shape[0]//2), (gray_image.shape[1]//2, gray_image.shape[1]//2)), mode='constant', constant_values=0)
        theta = np.linspace(0., 180., max(padded_image.shape), endpoint=False)
        sinogram = radon(padded_image, theta=theta)
        f.write(f"Radon Transform (sinogram) shape: {sinogram.shape}\n")

        # Write number of circles and contours
        f.write(f"Number of circles detected: {len(cx)}\n")
        f.write(f"Number of contours detected: {len(contours)}\n")

    # Function to convert images to uint8
    def convert_to_uint8(img):
        return (img * 255).astype(np.uint8)

    # Save results
    io.imsave(os.path.join(output_folder, 'smoothed_image.png'), convert_to_uint8(smoothed_image))
    io.imsave(os.path.join(output_folder, 'median_filtered_image.png'), convert_to_uint8(median_filtered_image))
    io.imsave(os.path.join(output_folder, 'denoised_image.png'), convert_to_uint8(denoised_image))
    io.imsave(os.path.join(output_folder, 'equalized_image.png'), convert_to_uint8(equalized_image))
    io.imsave(os.path.join(output_folder, 'clahe_image.png'), convert_to_uint8(clahe_image))
    io.imsave(os.path.join(output_folder, 'dilated.png'), convert_to_uint8(dilated))
    io.imsave(os.path.join(output_folder, 'eroded.png'), convert_to_uint8(eroded))
    io.imsave(os.path.join(output_folder, 'segmented_image.png'), convert_to_uint8(segmented_image))
    io.imsave(os.path.join(output_folder, 'rank_filtered_image.png'), convert_to_uint8(rank_filtered_image))
    io.imsave(os.path.join(output_folder, 'edges_canny.png'), convert_to_uint8(edges_canny))
    io.imsave(os.path.join(output_folder, 'edges_sobel.png'), convert_to_uint8(edges_sobel))
    io.imsave(os.path.join(output_folder, 'edges_laplace.png'), convert_to_uint8(edges_laplace))
    io.imsave(os.path.join(output_folder, 'edges_prewitt.png'), convert_to_uint8(edges_prewitt))
    io.imsave(os.path.join(output_folder, 'edges_roberts.png'), convert_to_uint8(edges_roberts))
    io.imsave(os.path.join(output_folder, 'edges_scharr.png'), convert_to_uint8(edges_scharr))
    io.imsave(os.path.join(output_folder, 'gabor_filtered.png'), convert_to_uint8(gabor_filtered_enhanced))

    # Save contour image
    contour_image = np.copy(gray_image)
    for contour in contours:
        plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
    plt.imshow(contour_image, cmap='gray')
    plt.axis('off')
    plt.savefig(os.path.join(output_folder, 'contours.png'), bbox_inches='tight', pad_inches=0)
    plt.close()

    # Save Harris corners image
    harris_image = np.copy(gray_image)
    plt.imshow(harris_image, cmap='gray')
    plt.plot(corners[:, 1], corners[:, 0], 'r.')
    plt.axis('off')
    plt.savefig(os.path.join(output_folder, 'harris_corners.png'), bbox_inches='tight', pad_inches=0)
    plt.close()

    # Save Hough circles image
    hough_circles_image = np.copy(image)
    plt.imshow(hough_circles_image, cmap='gray')
    for center_y, center_x, radius in zip(cy, cx, radii):
        circle = plt.Circle((center_x, center_y), radius, color='r', fill=False)
        plt.gca().add_patch(circle)
    plt.axis('off')
    plt.savefig(os.path.join(output_folder, 'hough_circles.png'), bbox_inches='tight', pad_inches=0)
    plt.close()


