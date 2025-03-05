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
    funnel_positions = np.zeros((num_drops, 2))  # Положение воронки (x_f, y_f)
    ball_positions = np.zeros((num_drops, 2))  # Положение шарика (x_b, y_b)

    # Начальное положение воронки в центре мишени (0, 0)
    funnel_positions[0] = [0, 0]

    # Симуляция первого падения шарика:
    # x_b[0] = x_f[0] + ε_x[0]
    # y_b[0] = y_f[0] + ε_y[0]
    ball_positions[0] = [
        funnel_positions[0, 0] + random_variations[0, 0],
        funnel_positions[0, 1] + random_variations[0, 1],
    ]

    # Симуляция оставшихся падений согласно правилам
    for i in range(1, num_drops):
        # Правило 1: не двигать воронку
        # x_f[i] = 0
        # y_f[i] = 0
        if rule_num == 1:
            funnel_positions[i] = [0, 0]

        # Правило 2: двигать воронку в противоположную сторону от последнего положения шарика
        # x_f[i] = x_f[i-1] - (x_b[i-1] - 0)
        # y_f[i] = y_f[i-1] - (y_b[i-1] - 0)
        elif rule_num == 2:
            funnel_positions[i] = [
                funnel_positions[i - 1, 0] - ball_positions[i - 1, 0],
                funnel_positions[i - 1, 1] - ball_positions[i - 1, 1],
            ]

        # Правило 3: двигать воронку от центра мишени в направлении,
        # противоположном отклонению шарика от центра
        # x_f[i] = -x_b[i-1]
        # y_f[i] = -y_b[i-1]
        elif rule_num == 3:
            funnel_positions[i] = [
                -ball_positions[i - 1, 0],
                -ball_positions[i - 1, 1],
            ]

        # Правило 4: ставить воронку туда, где остановился последний шарик
        # x_f[i] = x_b[i-1]
        # y_f[i] = y_b[i-1]
        elif rule_num == 4:
            funnel_positions[i] = ball_positions[i - 1].copy()

        # Симулируем падение шарика для всех правил:
        # x_b[i] = x_f[i] + ε_x[i]
        # y_b[i] = y_f[i] + ε_y[i]
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
