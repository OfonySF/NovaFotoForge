import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, exposure

def enhance_contrast(image, output_folder):
    image = np.array(image)
    # Function to apply transformations to each channel
    def apply_transformations(channel):
        equalized_channel = exposure.equalize_hist(channel)
        clahe_channel = exposure.equalize_adapthist(channel, clip_limit=0.03)
        log_channel = exposure.adjust_log(channel)
        gamma_channel = exposure.adjust_gamma(channel, gamma=0.5)
        inverted_channel = 1 - channel
        p2, p98 = np.percentile(channel, (2, 98))
        contrast_stretched_channel = exposure.rescale_intensity(channel, in_range=(p2, p98))
        exp_channel = exposure.adjust_sigmoid(channel, cutoff=0.5, gain=10)
        power_law_channel = exposure.adjust_gamma(channel, gamma=2.0)
        sigmoid_channel = exposure.adjust_sigmoid(channel, cutoff=0.5, gain=10)
        return [equalized_channel, clahe_channel, log_channel, gamma_channel, inverted_channel,
                contrast_stretched_channel, exp_channel, power_law_channel, sigmoid_channel]

    # Apply transformations to each channel
    transformed_images = [apply_transformations(image[..., i]) for i in range(image.shape[-1])]

    # Combine transformed channels back into images
    images = [
        (np.stack([transformed_images[0][0], transformed_images[1][0], transformed_images[2][0]], axis=-1), "Equalized Image"),
        (np.stack([transformed_images[0][1], transformed_images[1][1], transformed_images[2][1]], axis=-1), "CLAHE Image"),
        (np.stack([transformed_images[0][2], transformed_images[1][2], transformed_images[2][2]], axis=-1), "Log Image"),
        (np.stack([transformed_images[0][3], transformed_images[1][3], transformed_images[2][3]], axis=-1), "Gamma Image"),
        (np.stack([transformed_images[0][4], transformed_images[1][4], transformed_images[2][4]], axis=-1), "Inverted Image"),
        (np.stack([transformed_images[0][5], transformed_images[1][5], transformed_images[2][5]], axis=-1), "Contrast Stretched Image"),
        (np.stack([transformed_images[0][6], transformed_images[1][6], transformed_images[2][6]], axis=-1), "Exponential Image"),
        (np.stack([transformed_images[0][7], transformed_images[1][7], transformed_images[2][7]], axis=-1), "Power-Law Image"),
        (np.stack([transformed_images[0][8], transformed_images[1][8], transformed_images[2][8]], axis=-1), "Sigmoid Image")
    ]

    # Explanations for each transformation
    explanations = {
        "Equalized Image": "Выравнивание гистограммы улучшает контрастность изображения за счет распределения наиболее часто встречающихся значений интенсивности",
        "CLAHE Image": "CLAHE (Адаптивное выравнивание гистограммы с ограниченным контрастом) локально повышает контрастность изображения.",
        "Log Image": "Логарифмическая коррекция улучшает детали в темных областях изображения.",
        "Gamma Image": "Гамма-коррекция регулирует яркость изображения с помощью нелинейного преобразования.",
        "Inverted Image": "Инверсия изменяет значения интенсивности, создавая негатив изображения",
        "Contrast Stretched Image": "Контрастное растягивание улучшает контрастность за счет расширения диапазона значений интенсивности",
        "Exponential Image": "Экспоненциальное преобразование повышает контрастность с помощью экспоненциальной функции.",
        "Power-Law Image": "Степенное (гамма) преобразование регулирует контрастность изображения с помощью степенной функции.",
        "Sigmoid Image": "Коррекция сигмовидной формы повышает контрастность с помощью сигмовидной функции, подчеркивая среднюю интенсивность."
    }

    # Open a text file to write explanations
    with open(os.path.join(output_folder, "explanations.txt"), "w") as file:
        # Save histograms and explanations
        for i, (img, title) in enumerate(images):
            # Save image
            io.imsave(os.path.join(output_folder, f"{title.replace(' ', '_').lower()}.png"), (img * 255).astype(np.uint8))

            # Plot and save histogram for each color channel
            plt.figure()
            for channel, color in zip(range(img.shape[-1]), ['red', 'green', 'blue']):
                hist, bins = np.histogram(img[..., channel].ravel(), bins=256, range=(0, 1))
                plt.plot(bins[:-1], hist, color=color, label=f'{color.capitalize()} Channel')
            plt.title(f"{title} Histogram")
            plt.legend()
            plt.xlabel('Intensity Value')
            plt.ylabel('Frequency')
            plt.savefig(os.path.join(output_folder, f"{title.replace(' ', '_').lower()}_histogram.png"), bbox_inches='tight', pad_inches=0)
            plt.close()

            # Write explanation to file
            file.write(f"{title}:\n{explanations[title]}\n")
            file.write(f"Histogram Explanation: The histogram shows the distribution of pixel intensities for each color channel (Red, Green, Blue). Peaks indicate the most common intensity values, and the spread indicates the range of intensities present.\n\n")

    # Plot all images and their histograms
    fig, axes = plt.subplots(nrows=10, ncols=2, figsize=(14, 50))
    for i, (img, title) in enumerate(images):
        ax_img, ax_hist = axes[i]

        # Display image
        ax_img.imshow(img)
        ax_img.set_title(title)
        ax_img.axis('off')

        # Display histogram
        for channel, color in zip(range(img.shape[-1]), ['red', 'green', 'blue']):
            hist, bins = np.histogram(img[..., channel].ravel(), bins=256, range=(0, 1))
            ax_hist.plot(bins[:-1], hist, color=color, label=f'{color.capitalize()} Channel')
        ax_hist.set_title(f"{title} Histogram")
        ax_hist.legend()
        ax_hist.set_xlim(0, 1)
        ax_hist.set_xlabel('Intensity Value')
        ax_hist.set_ylabel('Frequency')

    plt.tight_layout(pad=3.0)
    plt.savefig(os.path.join(output_folder, "summary_output.png"))
    plt.show()


