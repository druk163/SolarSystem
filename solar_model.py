# coding: utf-8
# license: GPLv3

import math

gravitational_constant = 6.67408E-11


def calculate_force(body, space_objects):
    """Связывает планеты строго со своими звездами на основе порядка их считывания
    и рассчитывает угловую скорость вращения напрямую из параметра Vy.
    """
    if body.__class__.__name__.lower() == 'star':
        body.Vx = 0.0
        body.Vy = 0.0
        body.Fx = 0.0
        body.Fy = 0.0
        return

    if body.__class__.__name__.lower() == 'planet' and getattr(body, 'orbit_radius', 0) == 0:
        stars = [obj for obj in space_objects if obj.__class__.__name__.lower() == 'star']
        if len(stars) < 2:
            return

        all_planets = [obj for obj in space_objects if obj.__class__.__name__.lower() == 'planet']
        try:
            planet_index = all_planets.index(body)
        except ValueError:
            planet_index = 0

        # Жесткое разделение по ТЗ (7 к первой звезде, 13 ко второй)
        if planet_index < 7:
            closest_star = stars[0]
            orbit_index = planet_index + 1
        else:
            closest_star = stars[1]
            orbit_index = (planet_index - 7) + 1

        body.star = closest_star

        dx = body.x - closest_star.x
        dy = body.y - closest_star.y
        body.orbit_radius = (dx ** 2 + dy ** 2) ** 0.5
        body.angle = math.atan2(dy, dx)

        # Четные — по часовой (-1), нечетные — против (1)
        if orbit_index % 2 == 0:
            body.direction = -1
        else:
            body.direction = 1

        # Скорость рассчитывается на основе параметра Vy из файла
        linear_speed = abs(body.Vy)
        body.base_omega = linear_speed * 0.0000005


def move_space_object(body, dt, space_objects):
    """Смещает только планеты по окружности, предотвращая любые аварии."""
    if body.__class__.__name__.lower() == 'star':
        body.x = getattr(body, 'start_x', body.x)
        body.y = getattr(body, 'start_y', body.y)
        return

    if getattr(body, 'star', None) is not None and hasattr(body, 'base_omega'):
        tangential_force = 0.0
        tx = -math.sin(body.angle) * body.direction
        ty = math.cos(body.angle) * body.direction

        critical_distance = 11.0e9  # Барьер безопасности в метрах

        for other in space_objects:
            if other == body or other.__class__.__name__.lower() != 'planet':
                continue

            dx = other.x - body.x
            dy = other.y - body.y
            r = (dx ** 2 + dy ** 2) ** 0.5

            if r < 1e-5:
                continue

            # Мягкая фоновая гравитация Ньютона издалека
            r_soft = max(r, critical_distance)
            f_gravity = gravitational_constant * body.m * other.m / (r_soft ** 2)
            tangential_force += ((f_gravity * (dx / r_soft)) * tx + (f_gravity * (dy / r_soft)) * ty)

            # Экспоненциальный барьер против столкновений на пересечениях
            if r < critical_distance * 1.5:
                danger_factor = (critical_distance * 1.5 - r) / (critical_distance * 0.5)
                is_ahead = (dx * tx + dy * ty) > 0

                if is_ahead and body.m <= other.m:
                    tangential_force -= f_gravity * 15.0 * (danger_factor ** 3)
                elif not is_ahead and body.m > other.m:
                    tangential_force += f_gravity * 10.0 * (danger_factor ** 2)

        acceleration = tangential_force / body.m
        omega_perturbation = (acceleration / body.orbit_radius) * 1.5e5

        # Плавные лимиты торможения (до 95% сброса скорости для пропуска)
        if omega_perturbation > body.base_omega * 1.2:
            omega_perturbation = body.base_omega * 1.2
        elif omega_perturbation < -body.base_omega * 0.95:
            omega_perturbation = -body.base_omega * 0.95

        body.angle += (body.base_omega + omega_perturbation) * body.direction
        body.x = body.star.x + body.orbit_radius * math.cos(body.angle)
        body.y = body.star.y + body.orbit_radius * math.sin(body.angle)


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает геометрическое положение объектов без применения физики."""
    for body in space_objects:
        if body.__class__.__name__.lower() == 'star' and not hasattr(body, 'start_x'):
            body.start_x = body.x
            body.start_y = body.y
        calculate_force(body, space_objects)

    for body in space_objects:
        move_space_object(body, dt, space_objects)
