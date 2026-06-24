# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet

def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты."""
    objects = []
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue

            object_type = line.split()[0].lower()

            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print(f"Unknown space object: {object_type}")

    return objects

def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки."""
    parts = line.split()
    star.R = int(parts[1])
    star.color = parts[2]
    star.m = float(parts[3])
    star.x = float(parts[4])
    star.y = float(parts[5])
    star.Vx = float(parts[6])
    star.Vy = float(parts[7])

def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки."""
    parts = line.split()
    planet.R = int(parts[1])
    planet.color = parts[2]
    planet.m = float(parts[3])
    planet.x = float(parts[4])
    planet.y = float(parts[5])
    planet.Vx = float(parts[6])
    planet.Vy = float(parts[7])

def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл."""
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        for obj in space_objects:
            obj_type = obj.__class__.__name__.capitalize()
            out_file.write(
                f"{obj_type} {obj.R} {obj.color} {obj.m} "
                f"{obj.x} {obj.y} {obj.Vx} {obj.Vy}\n"
            )
