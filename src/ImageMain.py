# -*- coding: utf-8 -*-
#pillow
#opencv-python
#PyWavelets
#scikit-image
#scipy
#imageio
#tqdm
#matplotlib
#colorspacious
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance
import os
from process import process_images
#from Processing import start_processing

class ToolTip:
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

def Spravka():
    messagebox.showinfo("Метод Байса", "1. Параметры функции:\n\n  - 10: Параметр фильтрации для цветовых компонентов. Чем выше значение, тем больше шумоподавление, но это может привести к потере деталей.\n\n   - 10: - Параметр фильтрации для цветовых компонентов, аналогичен.\n\n   - 7: - Размер окна шаблона, используемого для поиска похожих пикселей. Это окно скользит по изображению и сравнивает центральный пиксель с окружающими. Значение 7 означает, что используется окно 7x7 пикселей.\n\n   - 21: - Размер окна поиска, в котором ищутся похожие пиксели для усреднения. Значение 21 означает, что используется окно 21x21 пикселей.\n\n2. Как работает алгоритм:\n\n   - Для каждого пикселя в изображении алгоритм берет окно шаблона размером 7x7 пикселей, центрированное на этом пикселе.\n   - Затем он ищет похожие окна в большем окне поиска размером 21x21 пикселей, также центрированном на текущем пикселе.\n   - Похожие пиксели (определяемые по цвету и интенсивности) усредняются, чтобы уменьшить шум, сохраняя при этом детали изображения.\n\n3. Откуда берутся пиксели:\n\n   - Пиксели берутся из окна поиска, которое охватывает область вокруг текущего пикселя. В данном случае, для каждого пикселя, алгоритм будет искать похожие пиксели в области 21x21 вокруг него.\n   - Если пиксель находится близко к краю изображения, алгоритм автоматически обрабатывает края, чтобы избежать выхода за пределы изображения.\n\n4. Расположение окна на изображении:\n\n   - Окно шаблона (7x7) и окно поиска (21x21) центрируются на каждом пикселе по очереди, начиная с верхнего левого угла изображения и заканчивая нижним правым.\n   - Алгоритм проходит по всему изображению, применяя описанный процесс к каждому пикселю.\n")
def SpravkaSR():
    messagebox.showinfo("Интрополяция", "Order 0 (Nearest-neighbor interpolation):\n\n- Описание: Это метод ближайшего соседа, который просто выбирает значение ближайшего пикселя без учета других соседних пикселей.\n\n - Преимущества: Быстрый и простой метод, не требует вычислений.- Недостатки: Может приводить к 'ступенчатым' артефактам и не подходит для изображений, где важна плавность.\n\n\nOrder 1 (Bilinear interpolation):\n\n- Описание: Использует линейное взвешивание четырех ближайших пикселей для вычисления нового значения пикселя.\n\n- Преимущества: Более гладкие результаты по сравнению с методом ближайшего соседа.\n\n- Недостатки: Может размывать изображение и не всегда сохраняет резкость.\n\n\nOrder 2 (Quadratic interpolation):\n\n- Описание: Использует квадратичные полиномы для интерполяции, учитывая большее количество соседних пикселей.\n\n- Преимущества: Более гладкие результаты, чем у билинейной интерполяции.\n\n- Недостатки: Более сложные вычисления, чем у билинейной интерполяции.\n\n\nOrder 3 (Cubic interpolation):\n\n- Описание: Использует кубические полиномы для интерполяции, что позволяет учитывать еще больше соседних пикселей.\n\n- Преимущества: Обеспечивает более гладкие и естественные результаты, чем билинейная интерполяция.\n\n- Недостатки: Более сложные вычисления и может быть медленнее.\n\n\nOrder 4 and higher (Higher-order spline interpolation):\n\n- Описание: Использует сплайны более высокого порядка для интерполяции.\n\n- Преимущества: Может давать очень гладкие результаты, особенно полезно для научных данных и изображений, где важна высокая точность.\n\n- Недостатки: Более сложные вычисления и может быть значительно медленнее.")


import tkinter as tk


def SpravkaAN():
    # Создание нового окна верхнего уровня
    top = tk.Toplevel()
    top.title("Анализ изображений")

    # Создание текстового виджета с вертикальным скроллбаром
    text_widget = tk.Text(top, wrap='word', width=100, height=40)
    scrollbar = tk.Scrollbar(top, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)

    # Упаковка текстового виджета и скроллбара
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Вставка информации в текстовый виджет
    info_text = (
        "Подготовка изображения:\n"
        "- Преобразует входное изображение в цифровой массив.\n"
        "- Проверяет наличие альфа-канала (прозрачность) и удаляет его, если он присутствует, оставляя только каналы RGB.\n"
        "- Преобразует изображение в оттенки серого для определенных операций.\n\n"

        "Сглаживание и фильтрация:\n"
        "- Фильтр Гаусса: Применяет фильтр Гаусса для сглаживания изображения, уменьшения шума и детализации.\n"
        "- Медианная фильтрация: Применяет медианный фильтр для дальнейшего уменьшения шума, что особенно полезно для устранения 'соленого' шума.\n"
        "- Вейвлет-шумоподавление: Использует вейвлет-преобразование для уменьшения шума изображения при сохранении краев.\n\n"

        "Повышение контрастности:\n"
        "- Выравнивание гистограммы: Повышает контрастность изображения в оттенках серого за счет увеличения значений интенсивности.\n"
        "- CLAHE: Локально повышает контрастность в небольших областях изображения.\n\n"

        "Морфологические операции:\n"
        "- Расширение и эрозия: Для обработки изображения используются морфологические операции, которые могут помочь в устранении небольших шумов и закрытии небольших отверстий в объектах.\n\n"

        "Сегментация:\n"
        "- SLIC: Разбивает изображение на суперпиксели, которые представляют собой области, похожие по цвету и текстуре.\n\n"

        "Определение границ:\n"
        "- Определяет края с помощью различных фильтров: Canny, Sobel, Laplace, Prewitt, Roberts и Scharr.\n\n"

        "Анализ текстур:\n"
        "- Фильтр Габора: Анализирует текстуру, применяя фильтр Габора, который полезен для определения определенных частотных и ориентационных компонентов.\n"
        "- GLCM: Вычисляет такие свойства текстуры, как контраст, непохожесть, энергия и однородность.\n"
        "- LBP: Анализ текстуры путем вычисления гистограммы локальных бинарных шаблонов.\n\n"

        "Анализ области и формы:\n"
        "- Свойства областей: Анализирует помеченные области на изображении для вычисления таких свойств, как площадь, периметр, эксцентриситет и компактность.\n"
        "- Определение углов: Использует детектор углов Harris для поиска углов на изображении.\n"
        "- Моменты Ху: Вычисляет моменты Ху для анализа формы, которые инвариантны к преобразованиям изображений.\n"
        "- Дескрипторы Фурье: Анализирует форму, используя дескрипторы Фурье контуров.\n\n"

        "Преобразование Хафа:\n"
        "- Круги: Определяет круги на изображении с помощью преобразования Хафа.\n"
        "- Линии: Определяет линии с помощью вероятностного преобразования Хафа.\n\n"

        "Преобразование Радона:\n"
        "- Вычисляет преобразование Радона (синограмму) изображения, что полезно для анализа проекций.\n\n"

        "Вывод:\n"
        "- Сохраняет различные обработанные изображения (например, сглаженные, отфильтрованные, сегментированные, с определением границ) в папку вывода.\n"
        "- Сохраняет визуализации контуров, углов и обнаруженных окружностей.\n"
        "- Записывает результаты анализа, такие как свойства текстуры и статистика областей, в текстовый файл.\n"
    )

    text_widget.insert(tk.END, info_text)
    text_widget.config(state=tk.DISABLED)  # Сделать текстовый виджет только для чтения



def SpravkaCO():
    # Создание нового окна верхнего уровня
    top = tk.Toplevel()
    top.title("Преобразование цветовой палитры")

    # Создание текстового виджета с вертикальным скроллбаром
    text_widget = tk.Text(top, wrap='word', width=100, height=40)
    scrollbar = tk.Scrollbar(top, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)

    # Упаковка текстового виджета и скроллбара
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Вставка информации в текстовый виджет
    info_text = (
        "Обработка изображений и преобразование цветовых пространств:\n"
        "- Программа загружает изображение и преобразует его в массив данных.\n"
        "- Если изображение содержит альфа-канал (прозрачность), он удаляется, оставляя только RGB-каналы.\n\n"

        "Преобразование в различные цветовые пространства:\n"
        "- Программа преобразует изображение в различные цветовые пространства, включая:\n"
        "  - Grayscale (оттенки серого)\n"
        "  - HSV (Hue, Saturation, Value)\n"
        "  - LAB (Lightness, A and B color components)\n"
        "  - YUV (Luminance and Chrominance)\n"
        "  - XYZ (CIE 1931 color space)\n"
        "  - HED (Hematoxylin, Eosin, DAB)\n"
        "  - LUV (CIE L*u*v* color space)\n"
        "  - YIQ (Luminance, In-phase, Quadrature)\n"
        "  - HSL (Hue, Saturation, Lightness)\n"
        "  - YCbCr (Luminance, Blue-difference, Red-difference)\n"
        "  - HSI (Hue, Saturation, Intensity)\n"
        "  - LCH (Lightness, Chroma, Hue) \n"
        "  - CMY (Cyan, Magenta, Yellow)\n"
        "  - YPbPr (Luminance, Blue-difference, Red-difference)\n"
        "- Преобразование в CMYK выполняется с использованием библиотеки PIL и сохраняется в формате TIFF.\n\n"

        "Сохранение и визуализация:\n"
        "- Все преобразованные изображения сохраняются в указанную папку вывода.\n"
        "- Изображения сохраняются в формате PNG, за исключением CMYK, который сохраняется в формате TIFF.\n"
        "- Программа визуализирует оригинальное изображение и все преобразованные версии в одном окне для сравнения.\n"
        "- Каждое изображение отображается с соответствующим заголовком, указывающим цветовое пространство.\n"
    )

    text_widget.insert(tk.END, info_text)
    text_widget.config(state=tk.DISABLED)  # Сделать текстовый виджет только для чтения

def SpravkaGIST():
    # Создание нового окна верхнего уровня
    top = tk.Toplevel()
    top.title("Построение гистограмм")

    # Создание текстового виджета с вертикальным скроллбаром
    text_widget = tk.Text(top, wrap='word', width=100, height=40)
    scrollbar = tk.Scrollbar(top, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)

    # Упаковка текстового виджета и скроллбара
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Вставка информации в текстовый виджет
    info_text = (

        "Преобразования изображения:\n"
        "- Выравнивание гистограммы (Equalized Image): Улучшает контрастность изображения за счет распределения наиболее часто встречающихся значений интенсивности.\n"
        "- CLAHE (CLAHE Image): Локально повышает контрастность изображения с помощью адаптивного выравнивания гистограммы с ограниченным контрастом.\n"
        "- Логарифмическая коррекция (Log Image): Улучшает детали в темных областях изображения.\n"
        "- Гамма-коррекция (Gamma Image): Регулирует яркость изображения с помощью нелинейного преобразования.\n"
        "- Инверсия (Inverted Image): Изменяет значения интенсивности, создавая негатив изображения.\n"
        "- Контрастное растягивание (Contrast Stretched Image): Улучшает контрастность за счет расширения диапазона значений интенсивности.\n"
        "- Экспоненциальное преобразование (Exponential Image): Повышает контрастность с помощью экспоненциальной функции.\n"
        "- Степенное преобразование (Power-Law Image): Регулирует контрастность изображения с помощью степенной функции.\n"
        "- Сигмовидная коррекция (Sigmoid Image): Повышает контрастность с помощью сигмовидной функции, подчеркивая среднюю интенсивность.\n\n"

        "Сохранение результатов:\n"
        "- Каждое преобразованное изображение сохраняется в указанной папке в формате PNG.\n"
        "- Для каждого изображения строится и сохраняется гистограмма, показывающая распределение интенсивностей пикселей для каждого цветового канала (красный, зеленый, синий).\n"
        "- Объяснения для каждого преобразования записываются в текстовый файл 'explanations.txt'.\n"
        "- Создается общий вывод всех изображений и их гистограмм, который сохраняется в файл 'summary_output.png'.\n"
    )

    text_widget.insert(tk.END, info_text)
    text_widget.config(state=tk.DISABLED)  # Сделать текстовый виджет только для чтения





def SpravkaGeo():
    # Create a new top-level window
    top = tk.Toplevel()
    top.title("Аффинные преобразования")

    # Create a Text widget with a vertical scrollbar
    text_widget = tk.Text(top, wrap='word', width=80, height=30)
    scrollbar = tk.Scrollbar(top, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)

    # Pack the Text widget and scrollbar
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Insert the information into the Text widget
    info_text = (
        "Масштабирование изображения:\n"
        "- rescale(img, scale=scale, anti_aliasing=anti_aliasing)\n"
        "- Описание: Изменяет размер изображения, увеличивая или уменьшая его в зависимости от заданного коэффициента scale. "
        "Параметр anti_aliasing помогает сгладить изображение после изменения размера.\n\n"
        "Поворот изображения:\n"
        "- rotate(img, angle=angle, resize=resize)\n"
        "- Описание: Поворачивает изображение на заданный угол angle. Параметр resize определяет, следует ли изменять размер изображения, чтобы сохранить все его части после поворота.\n\n"
        "Трансляция изображения:\n"
        "- warp(img, AffineTransform(translation=(tx, ty)), mode='wrap')\n"
        "- Описание: Перемещает изображение на tx пикселей вправо и ty пикселей вниз. Использует аффинное преобразование для выполнения сдвига, а mode='wrap' определяет, как обрабатывать пиксели за пределами границ изображения.\n\n"
        "Отражение изображения по горизонтали:\n"
        "- np.fliplr(img)\n"
        "- Описание: Отражает изображение по горизонтальной оси, создавая зеркальное отображение.\n\n"
        "Отражение изображения по вертикали:\n"
        "- np.flipud(img)\n"
        "- Описание: Отражает изображение по вертикальной оси, создавая зеркальное отображение.\n\n"
        "Обрезка изображения:\n"
        "- img[int(margin * img.shape[0]):int((1 - margin) * img.shape[0]), int(margin * img.shape[1]):int((1 - margin) * img.shape[1])]\n"
        "- Описание: Удаляет часть изображения по краям, оставляя центральную область. Параметр margin определяет долю изображения, которую следует обрезать с каждой стороны.\n\n"
        "Перспективное преобразование:\n"
        "- warp(img, ProjectiveTransform().estimate(src, dst), output_shape=(img.shape[0], img.shape[1]))\n"
        "- Описание: Изменяет перспективу изображения, используя точки src и dst для определения преобразования. Это позволяет создавать эффекты наклона или искажения.\n\n"
        "Поворот изображения с интерполяцией:\n"
        "- rotate(img, angle=angle, resize=resize, order=order)\n"
        "- Описание: Поворачивает изображение на заданный угол angle с использованием интерполяции порядка order. Параметр resize определяет, следует ли изменять размер изображения, чтобы сохранить все его части после поворота.\n\n"
        "Масштабирование изображения с разными коэффициентами:\n"
        "- rescale(img, scale=scale, anti_aliasing=anti_aliasing)\n"
        "- Описание: Изменяет размер изображения, увеличивая или уменьшая его в зависимости от заданного коэффициента scale. Параметр anti_aliasing помогает сгладить изображение после изменения размера.\n\n"
        "Диагональный сдвиг изображения:\n"
        "- warp(img, AffineTransform(shear=shear), mode='wrap')\n"
        "- Описание: Применяет диагональный сдвиг к изображению с использованием параметра shear. Это создает эффект наклона изображения. Параметр mode='wrap' определяет, как обрабатывать пиксели за пределами границ изображения.\n\n\n\n"
        "Масштабирование (1):\n"
        "- Параметры: scale, anti_aliasing\n"
        "- Пример: 1(2.0, True)\n\n"
        "Поворот (2):\n"
        "- Параметры: угол, изменение размера\n"
        "- Пример: 2(45, True)\n\n"
        "Перевод (3):\n"
        "- Параметры: tx, ty\n"
        "- Пример: 3(100, 50)\n\n"
        "Переворот по горизонтали (4):\n"
        "- Без параметров\n"
        "- Пример: 4()\n\n"
        "Переворот по вертикали (5):\n"
        "- Без параметров\n"
        "- Пример: 5()\n\n"
        "Обрезка (6):\n"
        "- Параметры: margin\n"
        "- Пример: 6(0.1)\n\n"
        "Проективное преобразование (7):\n"
        "- Параметры: src, dst\n"
        "- Пример: 7([[0, 0], [1, 0], [1, 1], [0, 1]], [[0, 0], [1, 0], [0.8, 1], [0.2, 1]])\n\n"
        "Расширенный поворот (8):\n"
        "- Параметры: угол, изменение размера, порядок\n"
        "- Пример: 8(30, True, 3)\n\n"
        "Асимметричное масштабирование (9):\n"
        "- Параметры: масштаб, сглаживание\n"
        "- Пример: 9((0.5, 1.5), True)\n\n"
        "Сдвиг (0):\n"
        "- Параметры: сдвиг\n"
        "- Пример: 0(0.5)\n\n\n"
        "1(scale, anti_aliasing) 2(angle, resize) 3(tx, ty) 4() 5() 6(margin) 7(src, dst) 8(angle, resize, order) 9(scale, anti_aliasing) 0(shear)\n\n"
    )

    text_widget.insert(tk.END, info_text)
    text_widget.config(state=tk.DISABLED)  # Make the text widget read-only



def start_processing():
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()
    extensions = extensions_var.get().split(',') if extensions_var.get() else None
    min_resolution = (int(min_width_var.get()), int(min_height_var.get()))
    name_contains = name_contains_var.get()
    change_name = change_name_var.get()
    change_format = change_format_var.get()
    change_resolution = (int(change_width_var.get()), int(change_height_var.get())) if change_width_var.get() and change_height_var.get() else None
    resolution_comparison = resolution_comparison_var.get()
    aspect_ratio = float(aspect_ratio_var.get()) if aspect_ratio_var.get() else None
    aspect_ratio_comparison = aspect_ratio_comparison_var.get()
    change_aspect_ratio = float(change_aspect_ratio_var.get()) if change_aspect_ratio_var.get() else None
    sharpness = float(sharpness_var.get())
    contrast = float(contrast_var.get())
    brightness = float(brightness_var.get())
    color = float(color_var.get())
    name_option = name_option_var.get()
    name_template = name_template_var.get()
    name_list_file = name_list_file_var.get()
    red_factor = float(red.get())
    green_factor = float(green.get())
    blue_factor = float(blue.get())
    denoise = name_option_menu_denoise_var.get()
    brightness_filter_strength = float(brightness_entry_denoise_var.get())
    color_filter_strength = float(color_entry_denoise_var.get())
    template_window_size = int(template_window_size_denoise_var.get())
    search_window_size = int(search_window_size_denoise_var.get())
    intrapolation_denoise = intrapolation_denoise_var.get()
    scale_factor_denoise = int(scale_factor_denoise_var.get())
    order_denoise = int(order_denoise_var.get())
    analisis = analisis_var.get()
    color_diff = color_diff_var.get()
    gist_diff = gist_diff_var.get()
    Geo = Geo_var.get()
    Geo_operand = str(Geo_operand_var.get())
    highlight_color = str(highlight_color_var.get())
    alpha = float(alpha_var.get())
    #super_resolution = int(super_resolution_var.get())
    #sr_model_path = sr_model_path_var.get()

    process_images(input_folder, output_folder, extensions, min_resolution, name_contains,
                   change_name, change_format, change_resolution, resolution_comparison,
                   aspect_ratio, aspect_ratio_comparison, change_aspect_ratio,
                   name_option, name_template, name_list_file,
                   sharpness, contrast, brightness, color, red_factor, green_factor, blue_factor, denoise,
                   brightness_filter_strength,  color_filter_strength,  template_window_size, search_window_size, intrapolation_denoise, scale_factor_denoise, order_denoise,
                   analisis, color_diff, gist_diff, Geo, Geo_operand, highlight_color, alpha)
                   #super_resolution, sr_model_path

def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_var.set(folder_selected)

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_var.set(folder_selected)

app = tk.Tk()
app.title("NovaFotoForge")

input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
extensions_var = tk.StringVar()
min_width_var = tk.StringVar(value='0')
min_height_var = tk.StringVar(value='0')
name_contains_var = tk.StringVar()
change_name_var = tk.StringVar()
change_format_var = tk.StringVar()
change_width_var = tk.StringVar()
change_height_var = tk.StringVar()
resolution_comparison_var = tk.StringVar(value='greater')
aspect_ratio_var = tk.StringVar()
aspect_ratio_comparison_var = tk.StringVar(value='equal')
change_aspect_ratio_var = tk.StringVar()
sharpness_var = tk.StringVar(value='1.0')
contrast_var = tk.StringVar(value='1.0')
brightness_var = tk.StringVar(value='1.0')
color_var = tk.StringVar(value='1.0')
name_option_var = tk.StringVar(value='replace')
name_template_var = tk.StringVar()
name_list_file_var = tk.StringVar()
blue = tk.StringVar(value='1.0')
green = tk.StringVar(value='1.0')
red = tk.StringVar(value='1.0')
name_option_menu_denoise_var = tk.StringVar(value='False')
search_window_size_denoise_var = tk.StringVar(value='21')
template_window_size_denoise_var = tk.StringVar(value='7')
color_entry_denoise_var = tk.StringVar(value='10.0')
brightness_entry_denoise_var = tk.StringVar(value='10.0')
intrapolation_denoise_var  = tk.StringVar(value='False')
scale_factor_denoise_var = tk.StringVar(value='1')
order_denoise_var = tk.StringVar(value='0')
analisis_var = tk.StringVar(value='False')
color_diff_var = tk.StringVar(value='False')
gist_diff_var = tk.StringVar(value='False')
Geo_var = tk.StringVar(value='False')
Geo_operand_var = tk.StringVar(value='1')
highlight_color_var = tk.StringVar(value='0,0,0')
alpha_var = tk.StringVar(value='0')


tk.Label(app, text="Входная папка:").grid(row=0, column=0, sticky='e')
input_folder_entry = tk.Entry(app, textvariable=input_folder_var, width=50)
input_folder_entry.grid(row=0, column=1)
ToolTip(input_folder_entry, "Введите путь к папке с изображениями: ")
tk.Button(app, text="Обзор", command=select_input_folder).grid(row=0, column=2)

tk.Label(app, text="Выходная папка:").grid(row=1, column=0, sticky='e')
output_folder_entry = tk.Entry(app, textvariable=output_folder_var, width=50)
output_folder_entry.grid(row=1, column=1)
ToolTip(output_folder_entry, "Введите путь к папке для сохранения обработанных изображений: ")
tk.Button(app, text="Обзор", command=select_output_folder).grid(row=1, column=2)

tk.Label(app, text="Расширения (через запятую):").grid(row=2, column=0, sticky='e')
extensions_entry = tk.Entry(app, textvariable=extensions_var)
extensions_entry.grid(row=2, column=1)
ToolTip(extensions_entry, "Введите расширения файлов для фильтрации (через запятую, например: .png,.jpg): ")

tk.Label(app, text="Минимальная ширина:").grid(row=3, column=0, sticky='e')
min_width_entry = tk.Entry(app, textvariable=min_width_var)
min_width_entry.grid(row=3, column=1)
ToolTip(min_width_entry, "Введите минимальную ширину изображения (0 для игнорирования):")

tk.Label(app, text="Минимальная высота:").grid(row=4, column=0, sticky='e')
min_height_entry = tk.Entry(app, textvariable=min_height_var)
min_height_entry.grid(row=4, column=1)
ToolTip(min_height_entry, "Введите минимальную высоту изображения (0 для игнорирования): ")

tk.Label(app, text="Сравнение разрешения:").grid(row=5, column=0, sticky='e')
resolution_comparison_menu = tk.OptionMenu(app, resolution_comparison_var, 'equal', 'greater', 'less', 'noequal')
resolution_comparison_menu.grid(row=5, column=1)
ToolTip(resolution_comparison_menu, "Выберите сравнение разрешения ('greater' для больше, 'less' для меньше, 'equal' для полного сравнения, 'noequal' для исколючения): ")

tk.Label(app, text="Соотношение сторон:").grid(row=6, column=0, sticky='e')
aspect_ratio_entry = tk.Entry(app, textvariable=aspect_ratio_var)
aspect_ratio_entry.grid(row=6, column=1)
ToolTip(aspect_ratio_entry, "Введите соотношение сторон (например, 1.5 для 3:2, оставьте пустым для игнорирования): ")

tk.Label(app, text="Сравнение соотношения сторон:").grid(row=7, column=0, sticky='e')
aspect_ratio_comparison_menu = tk.OptionMenu(app, aspect_ratio_comparison_var, 'equal', 'greater', 'less', 'noequal')
aspect_ratio_comparison_menu.grid(row=7, column=1)
ToolTip(aspect_ratio_comparison_menu, "Выберите сравнение соотношения сторон ('equal', 'greater', 'less', 'noequal'): ")


tk.Label(app, text="Имя содержит:").grid(row=8, column=0, sticky='e')
name_contains_entry = tk.Entry(app, textvariable=name_contains_var)
name_contains_entry.grid(row=8, column=1)
ToolTip(name_contains_entry, "Введите строку, которая должна содержаться в названии файла (оставьте пустым для игнорирования): ")


separator = ttk.Separator(app, orient='horizontal')
separator.grid(row=9, column=0, columnspan=3, sticky='ew', pady=10)


tk.Label(app, text="Изменить расширение:").grid(row=10, column=0, sticky='e')
change_format_entry = tk.Entry(app, textvariable=change_format_var)
change_format_entry.grid(row=10, column=1)
ToolTip(change_format_entry, "Введите новый формат для файлов (например, jpeg, оставьте пустым для игнорирования): \nПримеры форматов изображений, в которые можно конвертировать: JPEG, PNG, BMP, GIF, TIFF.\n")


tk.Label(app, text="Изменить ширину:").grid(row=11, column=0, sticky='e')
change_width_entry = tk.Entry(app, textvariable=change_width_var)
change_width_entry.grid(row=11, column=1)
ToolTip(change_width_entry, "Введите новую ширину изображения (оставьте пустым для игнорирования): ")

tk.Label(app, text="Изменить высоту:").grid(row=12, column=0, sticky='e')
change_height_entry = tk.Entry(app, textvariable=change_height_var)
change_height_entry.grid(row=12, column=1)
ToolTip(change_height_entry, "Введите новую высоту изображения (оставьте пустым для игнорирования): ")

tk.Label(app, text="Изменить соотношение сторон:").grid(row=13, column=0, sticky='e')
change_aspect_ratio_entry = tk.Entry(app, textvariable=change_aspect_ratio_var)
change_aspect_ratio_entry.grid(row=13, column=1)
ToolTip(change_aspect_ratio_entry, "Введите новое соотношение сторон (например, 1.5 для 3:2, оставьте пустым для игнорирования): ")


tk.Label(app, text="Изменить имя:").grid(row=14, column=0, sticky='e')
change_name_entry = tk.Entry(app, textvariable=change_name_var)
change_name_entry.grid(row=14, column=1)
ToolTip(change_name_entry, "Введите новое имя для файлов (оставьте пустым для игнорирования): ")

tk.Label(app, text="Вариант названия:").grid(row=15, column=0, sticky='e')
name_option_menu = tk.OptionMenu(app, name_option_var, 'appendL', 'appendR', 'replace', 'template', 'list')
name_option_menu.grid(row=15, column=1)
ToolTip(name_option_menu, "Выберите опцию для имени файла (append, replace, template, list):\n\n append:\n - Если выбрана эта опция, к исходному имени файла будет добавлена строка, указанная в change_name. (L-лево, R-Право)\nНапример, если исходное имя файла image.png и change_name=new (выбрано appendL), то новое имя будет imagenew.png\n\n replace:\n - Эта опция заменяет исходное имя файла на строку, указанную в change_name. Если change_name не указано, используется исходное имя файла.\nНапример, если change_name=newname, то файл будет сохранен как newname.png.\n\n template:\n - При использовании этой опции имя файла формируется на основе шаблона, указанного в name_template. Шаблон может содержать плейсхолдеры, такие как {index} для индекса файла и {original_name} для исходного имени файла.\nНапример, если name_template=image_{index}, то файлы будут именоваться как image_0.png, image_1.png и так далее.\n\n{index}: индекс текущего файла в процессе обработки. Это число, которое увеличивается с каждым новым файлом.\n\n{original_name}: исходное имя файла без расширения. Это позволяет сохранить часть оригинального имени в новом имени файла.\n\n{width}: ширина изображения. Это значение может быть полезно, если вы хотите включить информацию о размере изображения в имя файла.\n\n{height}: высота изображения. Аналогично ширине, это значение может быть включено в имя файла для дополнительной информации.\n\n{aspect_ratio}: соотношение сторон изображения, округленное до двух знаков после запятой. Это может быть полезно для указания пропорций изображения в имени файла.\n\n{extension}: расширение файла без точки. Это позволяет указать формат файла в имени, если это необходимо.\n\n list:\n - Если выбрана эта опция и указан файл со списком имен (name_list_file), то имена файлов будут браться из этого списка. Имена из списка применяются циклически, если количество файлов больше, чем количество имен в списке.\nНапример, если список имен содержит ['name1', 'name2'], то файлы будут именоваться как name1.png, name2.png, name1.png и так далее.\n")


tk.Label(app, text="Имя шаблона:").grid(row=16, column=0, sticky='e')
name_template_entry = tk.Entry(app, textvariable=name_template_var)
name_template_entry.grid(row=16, column=1)
ToolTip(name_template_entry, "Введите шаблон для имени файла (например, 'image_{index}', оставьте пустым для игнорирования): ")

tk.Label(app, text="Файл списка имен:").grid(row=17, column=0, sticky='e')
name_list_file_entry = tk.Entry(app, textvariable=name_list_file_var)
name_list_file_entry.grid(row=17, column=1)
ToolTip(name_list_file_entry, "Введите путь к файлу со списком имен (оставьте пустым для игнорирования): ")


tk.Label(app, text="Четкость:").grid(row=18, column=0, sticky='e')
sharpness_entry = tk.Entry(app, textvariable=sharpness_var)
sharpness_entry.grid(row=18, column=1)
ToolTip(sharpness_entry, "Введите уровень резкости (1.0 для игнорирования): ")

tk.Label(app, text="Контраст:").grid(row=19, column=0, sticky='e')
contrast_entry = tk.Entry(app, textvariable=contrast_var)
contrast_entry.grid(row=19, column=1)
ToolTip(contrast_entry, "Введите уровень контрастности (1.0 для игнорирования): ")

tk.Label(app, text="Яркость:").grid(row=20, column=0, sticky='e')
brightness_entry = tk.Entry(app, textvariable=brightness_var)
brightness_entry.grid(row=20, column=1)
ToolTip(brightness_entry, "Введите уровень яркости (1.0 для игнорирования): ")

tk.Label(app, text="Цвет:").grid(row=21, column=0, sticky='e')
color_entry = tk.Entry(app, textvariable=color_var)
color_entry.grid(row=21, column=1)
ToolTip(color_entry, "Введите уровень насыщенности цвета (1.0 для игнорирования): ")

tk.Label(app, text="Красный:").grid(row=22, column=0, sticky='e')
color_entry_red = tk.Entry(app, textvariable=red)
color_entry_red.grid(row=22, column=1)
ToolTip(color_entry_red, "Введите уровень насыщенности красного цвета (1.0 для игнорирования): ")

tk.Label(app, text="Зеленый:").grid(row=23, column=0, sticky='e')
color_entry_green = tk.Entry(app, textvariable=green)
color_entry_green.grid(row=23, column=1)
ToolTip(color_entry_green, "Введите уровень насыщенности зеленого цвета (1.0 для игнорирования): ")

tk.Label(app, text="Синий:").grid(row=24, column=0, sticky='e')
color_entry_blue = tk.Entry(app, textvariable=blue)
color_entry_blue.grid(row=24, column=1)
ToolTip(color_entry_blue, "Введите уровень насыщенности синего цвета (1.0 для игнорирования): ")


separator = ttk.Separator(app, orient='horizontal')
separator.grid(row=25, column=0, columnspan=3, sticky='ew', pady=10)



tk.Label(app, text="Фильтрации шумов методом Байеса:").grid(row=26, column=0, sticky='e')
name_option_menu_denoise = tk.OptionMenu(app, name_option_menu_denoise_var, 'True', 'False')
name_option_menu_denoise.grid(row=26, column=1)
ToolTip(name_option_menu_denoise, "Проводить фильтрацию шумов, если выбрано 'False', фильтрация не проводится")

tk.Label(app, text="Регулировка фильтрации яркости:").grid(row=27, column=0, sticky='e')
brightness_entry_denoise = tk.Entry(app, textvariable=brightness_entry_denoise_var)
brightness_entry_denoise.grid(row=27, column=1)
ToolTip(brightness_entry_denoise, "Параметр для регулировки фильтрации яркости. Чем выше значение, тем больше шумоподавление: ")

tk.Label(app, text="Регулировка фильтрации цвета:").grid(row=28, column=0, sticky='e')
color_entry_denoise = tk.Entry(app, textvariable=color_entry_denoise_var)
color_entry_denoise.grid(row=28, column=1)
ToolTip(color_entry_denoise, "Параметр для регулировки фильтрации цвета. Чем выше значение, тем больше шумоподавление: ")

tk.Label(app, text="Размера шаблона:").grid(row=29, column=0, sticky='e')
template_window_size_denoise = tk.Entry(app, textvariable=template_window_size_denoise_var)
template_window_size_denoise.grid(row=29, column=1)
ToolTip(template_window_size_denoise, "Размер окна шаблона, используемого для поиска похожих блоков. Значение по умолчанию — 7x7. Это окно определяет, насколько далеко алгоритм будет искать похожие блоки для усреднения: ")

tk.Label(app, text="Размера окна поиска:").grid(row=30, column=0, sticky='e')
search_window_size_denoise = tk.Entry(app, textvariable=search_window_size_denoise_var)
search_window_size_denoise.grid(row=30, column=1)
ToolTip(search_window_size_denoise, "Размер окна поиска, в котором алгоритм будет искать блоки, похожие на текущий блок. Значение по умолчанию — 21x21. Большее окно поиска может улучшить качество удаления шума, но увеличивает вычислительные затраты: ")

tk.Label(app, text="Цветовая маска:").grid(row=30, column=1, sticky='e')
highlight_color = tk.Entry(app, textvariable=highlight_color_var)
highlight_color.grid(row=30, column=2)
ToolTip(highlight_color, "Настройка цветовой палитры для RGB маски в фомате: `number,number,number` где number от 0 до 255 ")

tk.Label(app, text="Прозрачность маски:").grid(row=29, column=1, sticky='e')
alpha = tk.Entry(app, textvariable=alpha_var)
alpha.grid(row=29, column=2)
ToolTip(alpha, "Прозрачность маски от 0 до 1")



separator = ttk.Separator(app, orient='horizontal')
separator.grid(row=31, column=0, columnspan=3, sticky='ew', pady=10)


tk.Label(app, text="Интерполяционные методы расширения изображения:").grid(row=32, column=0, sticky='e')
intrapolation_denoise = tk.OptionMenu(app, intrapolation_denoise_var, 'True', 'False')
intrapolation_denoise.grid(row=32, column=1)
ToolTip(intrapolation_denoise, "Проводится расширение изображения, если выбрано 'False', расширение не проводится")

tk.Label(app, text="Размер расширения:").grid(row=33, column=0, sticky='e')
scale_factor_denoise = tk.Entry(app, textvariable=scale_factor_denoise_var)
scale_factor_denoise.grid(row=33, column=1)
ToolTip(scale_factor_denoise, "Размер расширения разрешения изображения, во сколько раз ее увеличить с востановлением качетсва, если оставить 1, изображение будет просто улучшено")

tk.Label(app, text="Порядок интерполяции:").grid(row=34, column=0, sticky='e')
order_denoise = tk.Entry(app, textvariable=order_denoise_var)
order_denoise.grid(row=34, column=1)
ToolTip(order_denoise, "Этот параметр определяет порядок интерполяции, используемой для изменения размера изображения")

separator = ttk.Separator(app, orient='horizontal')
separator.grid(row=35, column=0, columnspan=3, sticky='ew', pady=10)

tk.Label(app, text="Анализ изображения:").grid(row=36, column=0, sticky='e')
analisis = tk.OptionMenu(app, analisis_var, 'True', 'False')
analisis.grid(row=36, column=1)
ToolTip(analisis, "Проводится анализ изображения, если выбрано 'False', анализ не проводится")

tk.Label(app, text="Преобразование цветовой палитры:").grid(row=37, column=0, sticky='e')
color_diff = tk.OptionMenu(app, color_diff_var, 'True', 'False')
color_diff.grid(row=37, column=1)
ToolTip(color_diff, "Проводится изменение цветовой палитры изображения, если выбрано 'False', изменение не проводится")

tk.Label(app, text="Преобразование гистограммное:").grid(row=38, column=0, sticky='e')
gist_diff = tk.OptionMenu(app, gist_diff_var, 'True', 'False')
gist_diff.grid(row=38, column=1)
ToolTip(gist_diff, "Проводится гистограммное изменение, если выбрано 'False', изменение не проводится")

tk.Label(app, text="Аффинные преобразования:").grid(row=39, column=0, sticky='e')
Geo = tk.OptionMenu(app, Geo_var, 'True', 'False')
Geo.grid(row=39, column=1)
ToolTip(Geo, "Проводится аффинные преобразования, если выбрано 'False', преобразования не проводятся")

tk.Label(app, text="Аффинные операнды:").grid(row=40, column=0, sticky='e')
Geo_operand = tk.Entry(app, textvariable=Geo_operand_var)
Geo_operand.grid(row=40, column=1)
ToolTip(Geo_operand, "Слитная строка с операндами: ")



button = tk.Button(app, text="Начать обработку", command=start_processing)
button.grid(row=41, column=0, columnspan=3)
ToolTip(button, "Для копирования без изменений игнорируйте все поля")

button = tk.Button(app, text="Справка", command=SpravkaSR)
button.grid(row=32, column=2, columnspan=3)
ToolTip(button, "")

button = tk.Button(app, text="Справка", command=Spravka)
button.grid(row=26, column=2, columnspan=3)
ToolTip(button, "")

button = tk.Button(app, text="Справка", command=SpravkaAN)
button.grid(row=36, column=2, columnspan=3)
ToolTip(button, "")

button = tk.Button(app, text="Справка", command=SpravkaCO)
button.grid(row=37, column=2, columnspan=3)
ToolTip(button, "")

button = tk.Button(app, text="Справка", command=SpravkaGIST)
button.grid(row=38, column=2, columnspan=3)
ToolTip(button, "")

button = tk.Button(app, text="Справка", command=SpravkaGeo)
button.grid(row=39, column=2, columnspan=3)
ToolTip(button, "")


app.mainloop()

