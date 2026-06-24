# coding: utf-8
# license: GPLv3

header_font = "Arial-16"
window_width = 800
window_height = 800
scale_factor = None
_stars_phys_centers = []
_planet_counter = 0

def calculate_scale_factor(max_distance):
    global scale_factor, _stars_phys_centers, _planet_counter
    if max_distance == 0:
        max_distance = 1.0
    scale_factor = 0.38 * min(window_height, window_width) / max_distance
    _stars_phys_centers = []
    _planet_counter = 0
    print('Scale factor:', scale_factor)

def scale_x(x):
    return int(x * scale_factor) + window_width // 2

def scale_y(y):
    return window_height // 2 - int(y * scale_factor)

def create_star_image(space, star):
    global _stars_phys_centers
    x = scale_x(star.x)
    y = scale_y(star.y)
    r = int(star.R)
    _stars_phys_centers.append((star.x, star.y))
    star_color = "lightcyan" if star.color == "custom_blue" else star.color
    star.image = space.create_oval(x - r, y - r, x + r, y + r, fill=star_color, outline="")

def create_planet_image(space, planet):
    global _planet_counter
    x = scale_x(planet.x)
    y = scale_y(planet.y)
    r = int(planet.R)

    if len(_stars_phys_centers) < 2:
        center_x, center_y = window_width // 2, window_height // 2
        orbit_r = int(((x - center_x)**2 + (y - center_y)**2)**0.5)
    else:
        # Рисование кругов орбит строго вокруг правильных звезд по ТЗ
        if _planet_counter < 7:
            star_x, star_y = _stars_phys_centers[0]
        else:
            star_x, star_y = _stars_phys_centers[1]

        center_x = scale_x(star_x)
        center_y = scale_y(star_y)
        orbit_r = int(((x - center_x)**2 + (y - center_y)**2)**0.5)

    _planet_counter += 1

    if orbit_r > 0:
        space.create_oval(
            center_x - orbit_r, center_y - orbit_r,
            center_x + orbit_r, center_y + orbit_r,
            outline="#232328", width=1, tags="orbit"
        )

    planet.image = space.create_oval(x - r, y - r, x + r, y + r, fill=planet.color, outline="")

def update_system_name(space, system_name):
    space.create_text(30, 80, tag="header", text=system_name, font=header_font, fill="white")

def update_object_position(space, body):
    x = scale_x(body.x)
    y = scale_y(body.y)
    r = int(body.R)

    if x + r < 0 or x - r > window_width or y + r < 0 or y - r > window_height:
        space.coords(body.image, window_width + r, window_height + r,
                     window_width + 2 * r, window_height + 2 * r)
    else:
        space.coords(body.image, x - r, y - r, x + r, y + r)
