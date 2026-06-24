# coding: utf-8
# license: GPLv3

class Star:
    """Тип данных, описывающий звезду (статичную)."""

    def __init__(self):
        self.type = "star"
        self.m = 0.0
        self.x = 0.0  # Физическая координата центра X
        self.y = 0.0  # Физическая координата центра Y
        self.R = 5  # Экранный радиус в пикселях
        self.color = "red"
        self.image = None


class Planet:
    """Тип данных, описывающий планету с геометрическим вращением и поправками."""

    def __init__(self):
        self.type = "planet"
        self.m = 0.0
        self.x = 0.0
        self.y = 0.0
        self.R = 5
        self.color = "green"
        self.image = None

        # Параметры для стабильного вращения
        self.angle = 0.0  # Текущий угол планеты на орбите в радианах
        self.orbit_radius = 0.0  # Радиус орбиты в метрах
        self.speed = 0.0  # Текущая скорость изменения угла
        self.base_omega = 0.0  # Базовая скорость вращения из файла Vy
        self.direction = 1  # 1 — против часовой, -1 — по часовой
        self.star = None  # Ссылка на родительскую звезду
