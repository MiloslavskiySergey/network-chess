"""Chesss."""

from tkinter import Canvas, PhotoImage, Tk, font
from typing import Literal

from PIL import Image, ImageTk
from settings import IMAGES_DIR

from os.path import join
import inspect


left_desk = 50
botton_desk = 450
cell_size = 50

figures_name = [
    'Rook',
    'Knight',
    'Bishop',
    'Queen',
    'King',
    'Bishop',
    'Knight',
    'Rook'
]

columns_name = 'ABCDEFGH'
white_figures = []
white_pawn = []

black_figures = []
black_pawn = []

photo_images = []
flag_vid = False


def print_funcname() -> None:
    """Вывод имени текущей функции."""
    print(inspect.stack()[1][3])


def redraw_edge() -> None:
    """Перерисовать символы по краям доски."""
    canv.delete('let')
    for row in range(8):
        x1 = left_desk - 15
        y1 = botton_desk - (row + 0.5) * cell_size
        edge_text = f'{row + 1}' if not flag_vid else f'{8 - row}'
        canv.create_text(x1, y1, text=edge_text, font=d_font, tags='let')
        canv.create_text(x1 + 430, y1, text=edge_text, font=d_font, tags='let')

    for column in range(8):
        x1 = left_desk + (column + 0.5) * cell_size
        y1 = botton_desk + 15
        edge_text = columns_name[column] if not flag_vid else columns_name[7 - column]
        canv.create_text(x1, y1, text=edge_text, font=d_font, tags='let')
        canv.create_text(x1, y1 - 430, text=edge_text, font=d_font, tags='let')


def put_image(current_image, row: int, column: int) -> None:
    """Переместить рисунок в заднюю клетку доски."""
    image_x = left_desk + (column + 0.5) * cell_size
    image_y = botton_desk - (row + 0.5) * cell_size
    canv.coords(current_image, image_x, image_y)


def redraw_figures() -> None:
    """Перерисовать фигуры на доске."""
    if not flag_vid:
        for column in range(8):
            current_image = white_figures[column]
            put_image(current_image, 0, column)
            current_image = white_pawn[column]
            put_image(current_image, 1, column)

            current_image = white_figures[column]
            put_image(current_image, 7, column)
            current_image = white_pawn[column]
            put_image(current_image, 6, column)
    else:
        for column in range(8):
            current_image = black_figures[column]
            put_image(current_image, 7, column)
            current_image = black_pawn[column]
            put_image(current_image, 6, column)

            current_image = black_figures[column]
            put_image(current_image, 0, column)
            current_image = black_pawn[column]
            put_image(current_image, 1, column)


def redraw_desk() -> None:
    """Перерисовать доску."""
    redraw_edge()
    redraw_figures()


def load_image(file_name, images, row, column) -> Literal[1, 0]:
    """Загрузка изображения из файла."""
    global photo_images
    image_x = left_desk + (column + 0.5) * cell_size
    image_y = botton_desk - (row + 0.5) * cell_size
    try:
        photo_image = ImageTk.PhotoImage(Image.open(file_name))
        photo_images.append(photo_image)
        image = canv.create_image(image_x, image_y, image=photo_image)
        images.append(image)
        return 1
    except:  # noqa
        print(f'path error: {file_name}')
        return 0


root = Tk()
d_font = font.Font(family='helvetica', size=12)

rect_colors = ['#8D89AF', '#EFEF8E']

canv = Canvas(root, width=1000, height=600, bg='white')
canv.pack()
# нарисовать доску
for row in range(8):
    for column in range(8):
        x1 = left_desk + column * cell_size
        y1 = botton_desk - row * cell_size
        x2 = x1 + cell_size
        y2 = y1 - cell_size
        rect_color = rect_colors[(row + column) % 2]
        canv.create_rectangle(x1, y1, x2, y2, fill=rect_color)
# нарисовать нумерацию строк
for row in range(8):
    x1 = left_desk - 15
    y1 = botton_desk - (row + 0.5) * cell_size
    canv.create_text(x1, y1, text=f'{row + 1}', font=d_font, tags='let')
    canv.create_text(x1 + 430, y1, text=f'{row + 1}', font=d_font, tags='let')
# нарисовать обозначения колонок
for column in range(8):
    x1 = left_desk + (column + 0.5) * cell_size
    y1 = botton_desk + 15
    canv.create_text(x1, y1, text=columns_name[column], font=d_font, tags='let')
    canv.create_text(x1, y1 - 430, text=columns_name[column], font=d_font, tags='let')
# нарисовать внешний край доски
canv.create_rectangle(
    left_desk - 30,
    botton_desk + 30,
    left_desk + 430,
    botton_desk - 430
)
# нарисовать и отрисовать фигуры с пешками
for column in range(8):
    load_image(join(IMAGES_DIR, 'blackPawn.png'), black_pawn, 6, column)
    load_image(join(IMAGES_DIR, 'whitePawn.png'), white_pawn, 1, column)

    load_image(
        join(IMAGES_DIR, f'white{figures_name[column]}.png'),
        white_figures,
        0,
        column
    )

    load_image(
        join(IMAGES_DIR, f'black{figures_name[column]}.png'),
        black_figures,
        7,
        column
    )


def rotate_desk(event) -> None:
    """Перевернуть доску по шелчку."""
    global flag_vid
    flag_vid = True if not flag_vid else False  # noqa
    redraw_desk()


root.bind('<Button-3>', rotate_desk)
root.mainloop()
