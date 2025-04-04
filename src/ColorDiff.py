import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color
from PIL import Image
import colorspacious as cs

def rgb_to_hsi(image):
    # Normalize the RGB values to [0, 1]
    image = image / 255.0
    r, g, b = image[..., 0], image[..., 1], image[..., 2]
    intensity = (r + g + b) / 3.0

    # Calculate saturation
    min_rgb = np.minimum(np.minimum(r, g), b)
    saturation = 1 - (3 / (r + g + b + 1e-10)) * min_rgb

    # Calculate hue
    num = 0.5 * ((r - g) + (r - b))
    den = np.sqrt((r - g)**2 + (r - b) * (g - b))
    theta = np.arccos(num / (den + 1e-10))
    hue = np.where(b <= g, theta, 2 * np.pi - theta)
    hue = hue / (2 * np.pi)  # Normalize to [0, 1]

    hsi_image = np.stack((hue, saturation, intensity), axis=-1)
    return hsi_image

def rgb_to_ypbpr(image):
    # Normalize the RGB values to [0, 1]
    image = image / 255.0
    r, g, b = image[..., 0], image[..., 1], image[..., 2]

    # Conversion matrix for RGB to YPbPr
    y = 0.299 * r + 0.587 * g + 0.114 * b
    pb = -0.168736 * r - 0.331264 * g + 0.5 * b
    pr = 0.5 * r - 0.418688 * g - 0.081312 * b

    ypbpr_image = np.stack((y, pb, pr), axis=-1)
    return ypbpr_image

def convert_color_spaces(image, output_folder):
    image = np.array(image)
    if image.shape[-1] == 4:
        image = image[..., :3]
    gray_image = color.rgb2gray(image)
    hsv_image = color.rgb2hsv(image)
    lab_image = color.rgb2lab(image)
    yuv_image = color.rgb2yuv(image)
    xyz_image = color.rgb2xyz(image)
    hed_image = color.rgb2hed(image)
    luv_image = color.rgb2luv(image)
    yiq_image = color.rgb2yiq(image)
    hsl_image = color.rgb2hsv(image)  # Approximate HSL using HSV
    ycbcr_image = color.rgb2ycbcr(image)

    # Convert to CMYK using PIL
    pil_image = Image.fromarray((image * 255).astype(np.uint8))
    cmyk_image = pil_image.convert('CMYK')

    # Convert to HSI using custom function
    hsi_image = rgb_to_hsi(image)

    # Convert to LCH
    lch_image = cs.cspace_convert(image, "sRGB1", "CIELCh")

    # Convert to CMY
    cmy_image = 1 - image / 255.0

    # Convert to YPbPr using custom function
    ypbpr_image = rgb_to_ypbpr(image)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Function to convert images to uint8
    def convert_to_uint8(img):
        return (img * 255).astype(np.uint8)

    # Function to normalize images for display
    def normalize_for_display(img):
        img_min, img_max = img.min(), img.max()
        return (img - img_min) / (img_max - img_min)

    # Function to save images
    def save_image(img, filename):
        if img is not None:
            io.imsave(os.path.join(output_folder, filename), convert_to_uint8(img))

    # Save images in various color spaces
    save_image(gray_image, 'gray_image.png')
    save_image(hsv_image, 'hsv_image.png')
    save_image(lab_image, 'lab_image.png')
    save_image(yuv_image, 'yuv_image.png')
    save_image(xyz_image, 'xyz_image.png')
    save_image(hed_image, 'hed_image.png')
    save_image(luv_image, 'luv_image.png')
    save_image(hsl_image, 'hsl_image.png')
    save_image(ycbcr_image, 'ycbcr_image.png')
    save_image(yiq_image, 'yiq_image.png')
    save_image(hsi_image, 'hsi_image.png')
    save_image(lch_image, 'lch_image.png')
    save_image(cmy_image, 'cmy_image.png')
    save_image(ypbpr_image, 'ypbpr_image.png')

    # Save CMYK image in a format that supports CMYK, such as TIFF
    cmyk_image.save(os.path.join(output_folder, 'cmyk_image.tiff'))

    # Visualize results
    fig, axes = plt.subplots(1, 16, figsize=(85, 5))
    ax = axes.ravel()

    ax[0].imshow(image)
    ax[0].set_title("Original Image")

    ax[1].imshow(gray_image, cmap='gray')
    ax[1].set_title("Grayscale Image")

    ax[2].imshow(normalize_for_display(hsv_image))
    ax[2].set_title("HSV Image")

    ax[3].imshow(normalize_for_display(lab_image))
    ax[3].set_title("LAB Image")

    ax[4].imshow(normalize_for_display(yuv_image))
    ax[4].set_title("YUV Image")

    ax[5].imshow(normalize_for_display(xyz_image))
    ax[5].set_title("XYZ Image")

    ax[6].imshow(normalize_for_display(hed_image))
    ax[6].set_title("HED Image")

    ax[7].imshow(normalize_for_display(luv_image))
    ax[7].set_title("LUV Image")

    ax[8].imshow(normalize_for_display(hsl_image))
    ax[8].set_title("HSL Image")

    ax[9].imshow(normalize_for_display(ycbcr_image))
    ax[9].set_title("YCbCr Image")

    ax[10].imshow(normalize_for_display(yiq_image))
    ax[10].set_title("YIQ Image")

    ax[11].imshow(normalize_for_display(hsi_image))
    ax[11].set_title("HSI Image")

    ax[12].imshow(normalize_for_display(lch_image))
    ax[12].set_title("LCH Image")

    ax[13].imshow(np.array(cmyk_image))
    ax[13].set_title("CMYK Image")

    ax[14].imshow(normalize_for_display(cmy_image))
    ax[14].set_title("CMY Image")

    ax[15].imshow(normalize_for_display(ypbpr_image))
    ax[15].set_title("YPbPr Image")

    for a in ax:
        a.axis('off')

    plt.tight_layout()
    plt.show()

