# coding: utf-8
# license: GPLv3

import tkinter
import traceback
from solar_vis import *
from solar_model import *
from solar_input import *

perform_execution = True  # Автостарт включен
physical_time = 0
time_step_value = 15000.0
time_speed_value = 70.0
space_objects = []
show_orbits = True

def execution():
    global physical_time
    recalculate_space_objects_positions(space_objects, time_step_value)
    for body in space_objects:
        update_object_position(space, body)
    physical_time += time_step_value
    if perform_execution:
        space.after(101 - int(time_speed_value), execution)

def toggle_orbits_by_keypress(event):
    """Скрытие и показ орбит кнопкой Пробел на клавиатуре."""
    global show_orbits
    show_orbits = not show_orbits
    if show_orbits:
        space.itemconfig('orbit', state=tkinter.NORMAL)
    else:
        space.itemconfig('orbit', state=tkinter.HIDDEN)

def load_system_automatically(filename="solar_system.txt"):
    global space_objects
    try:
        space_objects = read_space_objects_data_from_file(filename)
        if not space_objects:
            return

        max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
        calculate_scale_factor(max_distance)

        for obj in space_objects:
            if obj.__class__.__name__.lower() == 'star':
                create_star_image(space, obj)

        for obj in space_objects:
            if obj.__class__.__name__.lower() == 'planet':
                create_planet_image(space, obj)

        if not show_orbits:
            space.itemconfig('orbit', state=tkinter.HIDDEN)
        print(f"Система успешно загружена из файла {filename}!")
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден в корне проекта.")
    except Exception as e:
        traceback.print_exc()

def main():
    global space
    root = tkinter.Tk()
    root.title("Solar System Simulation")
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)

    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(fill=tkinter.BOTH, expand=True)

    root.bind("<space>", toggle_orbits_by_keypress)
    load_system_automatically("solar_system.txt")
    execution()
    root.mainloop()

if __name__ == "__main__":
    main()
