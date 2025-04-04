import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.transform import rescale, rotate, AffineTransform, warp, ProjectiveTransform
import re

def parse_parameters(param_str):
    # Извлечение параметров из строки
    params = re.findall(r'\((.*?)\)', param_str)
    if params:
        return eval(params[0])  # Преобразование строки в кортеж
    return ()

def geometric_transformations(image, operations, output_folder):
    image = np.array(image)
    transformed_image = image.copy()

    # Определение функций преобразования
    transformations = {
        '1': lambda img, scale, anti_aliasing, channel_axis: rescale(img, scale=scale, anti_aliasing=anti_aliasing, channel_axis=-1),
        '2': lambda img, angle, resize: rotate(img, angle=angle, resize=resize),
        '3': lambda img, tx, ty: warp(img, AffineTransform(translation=(tx, ty)), mode='wrap'),
        '4': lambda img: np.fliplr(img),
        '5': lambda img: np.flipud(img),
        '6': lambda img, margin: img[int(margin * img.shape[0]):int((1 - margin) * img.shape[0]), int(margin * img.shape[1]):int((1 - margin) * img.shape[1])],
        '7': lambda img, src, dst: warp(img, ProjectiveTransform().estimate(src, dst), output_shape=(img.shape[0], img.shape[1])),
        '8': lambda img, angle, resize, order: rotate(img, angle=angle, resize=resize, order=order),
        '9': lambda img, scale, anti_aliasing, channel_axis: rescale(img, scale=scale, anti_aliasing=anti_aliasing, channel_axis=-1),
        '0': lambda img, shear: warp(img, AffineTransform(shear=shear), mode='wrap')
    }

    # Применение преобразований в порядке, указанном в operations
    for op in operations.split(')'):
        if op:
            op_code = op[0]
            params = parse_parameters(op[1:] + ')')
            if op_code in transformations:
                transformed_image = transformations[op_code](transformed_image, *params)

    # Сохранение преобразованного изображения
    output_path = os.path.join(output_folder, 'transformed_image.png')
    io.imsave(output_path, (transformed_image * 255).astype(np.uint8))

    # Отображение оригинального и преобразованного изображения
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    ax = axes.ravel()

    ax[0].imshow(image)
    ax[0].set_title("Original Image")
    ax[0].axis('off')

    ax[1].imshow(transformed_image)
    ax[1].set_title("Transformed Image")
    ax[1].axis('off')

    plt.tight_layout()
    plt.show()
