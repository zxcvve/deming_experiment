import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random

# Настройка параметров эксперимента
NUM_DROPS = 50  # Количество бросков для каждого правила
NOISE_STDDEV = 1.0  # Стандартное отклонение для случайности падения шарика

# Предварительно генерируем случайные отклонения, которые будут использоваться для всех правил
np.random.seed(42)  # Для воспроизводимости результатов
random_variations = np.random.normal(0, NOISE_STDDEV, (NUM_DROPS, 2))


# Функция для симуляции одного правила
def simulate_rule(rule_num, num_drops, random_variations):
    # Инициализация координат
    funnel_positions = np.zeros((num_drops, 2))  # Положение воронки
    ball_positions = np.zeros((num_drops, 2))  # Положение шарика

    # Начальное положение воронки в центре мишени (0, 0)
    funnel_positions[0] = [0, 0]

    # Симуляция первого падения шарика с использованием предварительно сгенерированной вариации
    ball_positions[0] = [
        funnel_positions[0, 0] + random_variations[0, 0],
        funnel_positions[0, 1] + random_variations[0, 1],
    ]

    # Симуляция оставшихся падений согласно правилам
    for i in range(1, num_drops):
        # Правило 1: не двигать воронку
        if rule_num == 1:
            funnel_positions[i] = [0, 0]  # Воронка всегда в центре

        # Правило 2: двигать воронку в противоположную сторону от последнего положения шарика
        # относительно центра мишени
        elif rule_num == 2:
            # Вычисляем отклонение шарика от центра мишени (0,0)
            deviation_x = ball_positions[i - 1, 0] - 0  # 0 - это центр мишени
            deviation_y = ball_positions[i - 1, 1] - 0

            # Двигаем воронку в противоположном направлении от её текущего положения
            funnel_positions[i] = [
                funnel_positions[i - 1, 0] - deviation_x,
                funnel_positions[i - 1, 1] - deviation_y,
            ]

        # Правило 3: двигать воронку от центра мишени в направлении,
        # противоположном отклонению шарика от центра
        elif rule_num == 3:
            # Вычисляем отклонение шарика от центра
            deviation_x = ball_positions[i - 1, 0] - 0  # 0 - это центр мишени
            deviation_y = ball_positions[i - 1, 1] - 0

            # Устанавливаем воронку в противоположном направлении от центра
            funnel_positions[i] = [-deviation_x, -deviation_y]

        # Правило 4: ставить воронку туда, где остановился последний шарик
        elif rule_num == 4:
            funnel_positions[i] = ball_positions[i - 1].copy()

        # Симулируем падение шарика, используя ту же самую случайную вариацию для всех правил
        ball_positions[i] = [
            funnel_positions[i, 0] + random_variations[i, 0],
            funnel_positions[i, 1] + random_variations[i, 1],
        ]

    return funnel_positions, ball_positions


# Симуляция всех четырех правил с одинаковыми случайными вариациями
results = {}
for rule in range(1, 5):
    funnel_pos, ball_pos = simulate_rule(rule, NUM_DROPS, random_variations)
    results[rule] = {"funnel": funnel_pos, "ball": ball_pos}

# Визуализация результатов
fig, axes = plt.subplots(2, 2, figsize=(15, 15))
axes = axes.flatten()

for rule in range(1, 5):
    ax = axes[rule - 1]
    funnel_pos = results[rule]["funnel"]
    ball_pos = results[rule]["ball"]

    # Рисуем мишень
    target = Circle((0, 0), 1, fill=False, color="red")
    ax.add_patch(target)
    target = Circle((0, 0), 2, fill=False, color="blue")
    ax.add_patch(target)
    target = Circle((0, 0), 3, fill=False, color="green")
    ax.add_patch(target)

    # Рисуем траекторию воронки
    ax.plot(
        funnel_pos[:, 0], funnel_pos[:, 1], "b-", alpha=0.3, label="Траектория воронки"
    )

    # Рисуем положения шариков
    ax.scatter(
        ball_pos[:, 0],
        ball_pos[:, 1],
        c=range(NUM_DROPS),
        cmap="viridis",
        alpha=0.7,
        label="Положения шарика",
    )

    # Добавляем стрелки для показа последовательности
    for i in range(min(10, NUM_DROPS - 1)):
        ax.annotate(
            "",
            xy=(ball_pos[i + 1, 0], ball_pos[i + 1, 1]),
            xytext=(ball_pos[i, 0], ball_pos[i, 1]),
            arrowprops=dict(arrowstyle="->", color="gray"),
            alpha=0.7,
        )

    # Настраиваем ось
    ax.set_aspect("equal")
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.grid(True)
    ax.set_title(f"Правило {rule}")
    ax.set_xlabel("X координата")
    ax.set_ylabel("Y координата")
    ax.legend()

# Добавляем дополнительную статистику
for rule in range(1, 5):
    # Вычисляем среднее отклонение шариков от центра
    ball_pos = results[rule]["ball"]
    distances = np.sqrt(ball_pos[:, 0] ** 2 + ball_pos[:, 1] ** 2)
    avg_distance = np.mean(distances)
    std_distance = np.std(distances)

    # Добавляем текст с результатами на графики
    axes[rule - 1].text(
        0.05,
        0.95,
        f"Среднее расстояние от центра: {avg_distance:.2f}\n"
        f"Стд. отклонение: {std_distance:.2f}",
        transform=axes[rule - 1].transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

plt.tight_layout()
plt.savefig("deming_funnel_experiment.png", dpi=300)
plt.show()

# Общая таблица результатов
print("Результаты эксперимента Деминга:")
print("=" * 60)
print(f"{'Правило':<10} {'Среднее расстояние':<20} {'Стд. отклонение':<20}")
print("-" * 60)
for rule in range(1, 5):
    ball_pos = results[rule]["ball"]
    distances = np.sqrt(ball_pos[:, 0] ** 2 + ball_pos[:, 1] ** 2)
    avg_distance = np.mean(distances)
    std_distance = np.std(distances)
    print(f"{rule:<10} {avg_distance:<20.2f} {std_distance:<20.2f}")
print("=" * 60)
