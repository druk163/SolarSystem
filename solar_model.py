# coding: utf-8
# license: GPLv3

import math

gravitational_constant = 6.67408E-11

def calculate_force(body, space_objects):
    """Связывает планеты строго со своими звездами и задает им строго
    уникальные рассинхронизированные скорости, чтобы исключить столкновения.
    """
    if body.__class__.__name__.lower() == 'star':
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

        # Разделение планет между звездами
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

        # Направление вращения
        if orbit_index % 2 == 0:
            body.direction = -1
        else:
            body.direction = 1

        # Формула уникальной скорости: подмешиваем индекс планеты, 
        # чтобы периоды обращения никогда не совпадали кратно
        linear_speed = abs(body.Vy)
        body.base_omega = (linear_speed * 0.0000005) * (1.0 + (planet_index * 0.07))


def move_space_object(body, dt, space_objects):
    """Смещает планеты по орбитам с проверкой наложения."""
    if body.__class__.__name__.lower() == 'star':
        body.x = getattr(body, 'start_x', body.x)
        body.y = getattr(body, 'start_y', body.y)
        return

    if getattr(body, 'star', None) is not None and hasattr(body, 'base_omega'):
        current_omega = body.base_omega
        critical_distance = 25.0e9  # Дистанция безопасного разъезда

        # Вычисляем гипотетический следующий шаг
        next_angle = body.angle + current_omega * body.direction
        next_x = body.star.x + body.orbit_radius * math.cos(next_angle)
        next_y = body.star.y + body.orbit_radius * math.sin(next_angle)

        slow_down = False
        for other in space_objects:
            if other == body or other.__class__.__name__.lower() != 'planet':
                continue

            # Смотрим, пересекаемся ли мы на следующем шаге с текущим положением другой планеты
            dx = other.x - next_x
            dy = other.y - next_y
            r = (dx ** 2 + dy ** 2) ** 0.5

            if r < critical_distance:
                # Проверяем, идет ли другая планета впереди нас
                tx = -math.sin(body.angle) * body.direction
                ty = math.cos(body.angle) * body.direction
                p_dx = other.x - body.x
                p_dy = other.y - body.y
                
                if (p_dx * tx + p_dy * ty) > 0:
                    slow_down = True
                    break

        if slow_down:
            # Если впереди планета — притормаживаем до минимума, пропуская её
            body.angle += (current_omega * 0.1) * body.direction
        else:
            body.angle = next_angle

        body.x = body.star.x + body.orbit_radius * math.cos(body.angle)
        body.y = body.star.y + body.orbit_radius * math.sin(body.angle)


def recalculate_space_objects_positions(space_objects, dt):
    for body in space_objects:
        if body.__class__.__name__.lower() == 'star' and not hasattr(body, 'start_x'):
            body.start_x = body.x
            body.start_y = body.y
        calculate_force(body, space_objects)

    for body in space_objects:
        move_space_object(body, dt, space_objects)