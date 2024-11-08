import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Ввод параметров системы
mass1 = float(input("Масса первого тела (кг): "))
mass2 = float(input("Масса второго тела (кг): "))
speed1 = float(input("Скорость первого тела (м/с): "))
speed2 = float(input("Скорость второго тела (м/с): "))
direction1 = np.array(list(map(float, input("Вектор направления первого тела (x, y): ").split(','))))
direction2 = np.array(list(map(float, input("Вектор направления второго тела (x, y): ").split(','))))
box_height = float(input("Высота оболочки: "))
box_width = float(input("Ширина оболочки: "))

# Начальные скорости, нормализованные по направлениям
velocity1 = direction1 / np.linalg.norm(direction1) * speed1
velocity2 = direction2 / np.linalg.norm(direction2) * speed2

# Начальные позиции тел
pos1 = np.array([1.0, 1.0])
pos2 = np.array([box_width - 1.0, box_height - 1.0])

# Временные параметры
dt = 0.01
duration = 20

# Массивы для хранения данных
positions = [pos1, pos2]
velocities = [velocity1, velocity2]
masses = [mass1, mass2]

# Функция для расчета столкновения
def compute_collision(v1, v2, m1, m2, p1, p2):
    direction = (p2 - p1) / np.linalg.norm(p2 - p1)
    impulse = 2 * (np.dot(v1 - v2, direction)) / (m1 + m2)
    v1_new = v1 - impulse * m2 * direction
    v2_new = v2 + impulse * m1 * direction
    return v1_new, v2_new

# Функция для обновления позиций
def update_positions():
    global positions, velocities

    # Обновление позиций и проверка столкновений с границами
    for i in range(2):
        positions[i] += velocities[i] * dt
        if positions[i][0] <= 0 or positions[i][0] >= box_width:
            velocities[i][0] *= -1
        if positions[i][1] <= 0 or positions[i][1] >= box_height:
            velocities[i][1] *= -1

    # Проверка столкновения тел
    if np.linalg.norm(positions[0] - positions[1]) < 0.5:
        velocities[0], velocities[1] = compute_collision(
            velocities[0], velocities[1], masses[0], masses[1], positions[0], positions[1]
        )

# Создание окна для анимации с тёмным фоном
fig, ax = plt.subplots()
ax.set_facecolor('#1e1e1e')  # Цвет фона оболочки
ax.set_xlim(0, box_width)
ax.set_ylim(0, box_height)

# Создание тел с яркими цветами и тенью для более красивой визуализации
ball1 = plt.Circle(positions[0], 0.25, fc='#ff6361', edgecolor='black', linewidth=1.2, alpha=0.9)
ball2 = plt.Circle(positions[1], 0.25, fc='#ffa600', edgecolor='black', linewidth=1.2, alpha=0.9)
ax.add_patch(ball1)
ax.add_patch(ball2)

# Текст для отображения массы и скорости с цветом, контрастирующим с фоном
mass_text1 = ax.text(*positions[0], f'{mass1:.1f} кг', ha='center', va='center', color='#ffffff', fontsize=10, weight='bold')
mass_text2 = ax.text(*positions[1], f'{mass2:.1f} кг', ha='center', va='center', color='#ffffff', fontsize=10, weight='bold')
speed_text1 = ax.text(positions[0][0], positions[0][1] - 0.4, f'{np.linalg.norm(velocity1):.2f} м/с', ha='center', color='#ff6361')
speed_text2 = ax.text(positions[1][0], positions[1][1] - 0.4, f'{np.linalg.norm(velocity2):.2f} м/с', ha='center', color='#ffa600')

# Функция анимации
def animate(frame):
    update_positions()
    ball1.set_center(positions[0])
    ball2.set_center(positions[1])

    mass_text1.set_position(positions[0])
    mass_text2.set_position(positions[1])
    speed_text1.set_position((positions[0][0], positions[0][1] - 0.4))
    speed_text2.set_position((positions[1][0], positions[1][1] - 0.4))
    speed_text1.set_text(f'{np.linalg.norm(velocities[0]):.2f} м/с')
    speed_text2.set_text(f'{np.linalg.norm(velocities[1]):.2f} м/с')
    return ball1, ball2, mass_text1, mass_text2, speed_text1, speed_text2

# Настройка и запуск анимации
anim = FuncAnimation(fig, animate, frames=int(duration / dt), interval=20, blit=True)

# Сохранение анимации как GIF
anim.save("simulation.gif", writer=PillowWriter(fps=50))
plt.close()