from PIL import Image, ImageEnhance
import os
from tkinter import messagebox
import cv2
import numpy as np
import imageio.v2 as imageio
from scipy.ndimage import zoom
from AnalPost import combined_image_analysis
from ColorDiff import convert_color_spaces
from Gist import enhance_contrast
from Geometry import geometric_transformations
from BinVector import binary_vectorization_with_color
def process_images(input_folder, output_folder, extensions=None, min_resolution=(0, 0), name_contains=None,
                   change_name=None, change_format=None, change_resolution=None, resolution_comparison='greater',
                   aspect_ratio=None, aspect_ratio_comparison='equal', change_aspect_ratio=None,
                   name_option='replace', name_template=None, name_list_file=None,
                   sharpness=1.0, contrast=1.0, brightness=1.0, color=1.0,
                   red_factor=1.0, green_factor=1.0, blue_factor=1.0, denoise='False', brightness_filter_strength=10,
                   color_filter_strength=10, template_window_size=7, search_window_size=21, intrapolation_denoise='False', scale_factor_denoise=1,
                   order_denoise=0, analisis='False', color_diff='False', gist_diff ='False', Geo='False', Geo_operand = '', highlight_color = "0,0,0", alpha = 0):
                   #super_resolution=False, sr_model_path=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    name_list = []
    if name_list_file:
        with open(name_list_file, 'r') as f:
            name_list = [line.strip() for line in f.readlines()]

    total_original_size = 0
    total_processed_size = 0

    # Load super-resolution model if enabled


    for index, filename in enumerate(os.listdir(input_folder)):
        file_path = os.path.join(input_folder, filename)
        if extensions and not filename.lower().endswith(tuple(extensions)):
            continue
        if name_contains and name_contains not in filename:
            continue

        with Image.open(file_path) as img:
            width, height = img.size
            current_aspect_ratio = width / height
            original_size = os.path.getsize(file_path)
            total_original_size += original_size

            if resolution_comparison == 'equal':
                if width != min_resolution[0] or height != min_resolution[1]:
                    continue
            elif resolution_comparison == 'greater':
                if width < min_resolution[0] or height < min_resolution[1]:
                    continue
            elif resolution_comparison == 'noequal':
                if width == min_resolution[0] or height == min_resolution[1]:
                    continue
            elif resolution_comparison == 'less':
                if width > min_resolution[0] or height > min_resolution[1]:
                    continue

            if aspect_ratio is not None:
                if aspect_ratio_comparison == 'equal' and current_aspect_ratio != aspect_ratio:
                    continue
                elif aspect_ratio_comparison == 'greater' and current_aspect_ratio <= aspect_ratio:
                    continue
                elif aspect_ratio_comparison == 'less' and current_aspect_ratio >= aspect_ratio:
                    continue
                elif aspect_ratio_comparison == 'noequal' and current_aspect_ratio == aspect_ratio:
                    continue

            if change_aspect_ratio:
                new_width = width
                new_height = height
                if current_aspect_ratio > change_aspect_ratio:
                    new_width = int(height * change_aspect_ratio)
                else:
                    new_height = int(width / change_aspect_ratio)
                img = img.crop(((width - new_width) // 2, (height - new_height) // 2,
                                (width + new_width) // 2, (height + new_height) // 2))

            img = ImageEnhance.Sharpness(img).enhance(sharpness)
            img = ImageEnhance.Contrast(img).enhance(contrast)
            img = ImageEnhance.Brightness(img).enhance(brightness)
            img = ImageEnhance.Color(img).enhance(color)

            r, g, b = img.split()
            r = r.point(lambda i: i * red_factor)
            g = g.point(lambda i: i * green_factor)
            b = b.point(lambda i: i * blue_factor)
            img = Image.merge('RGB', (r, g, b))

            if denoise == "True":
             img = binary_vectorization_with_color(img, highlight_color, alpha, denoise,
                                            brightness_filter_strength, color_filter_strength, template_window_size,
                                            search_window_size)



            base_name, ext = os.path.splitext(filename)
            if name_option == 'appendL':
                new_filename = base_name + (change_name or '') + ext
            elif name_option == 'appendR':
                new_filename = (change_name or '') + base_name + ext
            elif name_option == 'replace':
                new_filename = (change_name or base_name) + ext
            elif name_option == 'template' and name_template:
                new_filename = name_template.format(index=index, original_name=base_name, width=width, height=height,
                                                    aspect_ratio=f"{current_aspect_ratio:.2f}", extension=ext.strip('.')) + ext
            elif name_option == 'list' and name_list:
                new_filename = name_list[index % len(name_list)] + ext
            else:
                new_filename = filename

            if change_format:
                new_filename = os.path.splitext(new_filename)[0] + '.' + change_format
                img = img.convert("RGB")

            if change_resolution:
                img = img.resize(change_resolution, Image.LANCZOS)

            if intrapolation_denoise:
                img_np = np.array(img)
                img_np = zoom(img_np, (scale_factor_denoise, scale_factor_denoise, 1), order=order_denoise)
                if img_np.dtype == np.float32 or img_np.dtype == np.float64:
                    # Если изображение в формате с плавающей точкой, нормализуем его в диапазон [0, 255]
                    img_np = (img_np * 255).clip(0, 255).astype(np.uint8)
                else:
                    # Если изображение уже в формате uint8, сохраняем его напрямую
                    img_np = img_np.astype(np.uint8)
                img = Image.fromarray(img_np)

            if analisis == 'True':
                    combined_image_analysis( img,output_folder)

            if color_diff == 'True':
                    convert_color_spaces(img,output_folder)

            if gist_diff == 'True':
                    enhance_contrast(img,output_folder)

            if Geo == 'True':
                    geometric_transformations(img, Geo_operand ,output_folder)


            output_path = os.path.join(output_folder, new_filename)
            img.save(output_path)

            processed_size = os.path.getsize(output_path)
            total_processed_size += processed_size

    messagebox.showinfo("Processing Complete", f"Total original size: {total_original_size} bytes\nTotal processed size: {total_processed_size} bytes")
