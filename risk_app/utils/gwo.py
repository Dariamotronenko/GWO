import random
from .risk_score import calculate_risk_score

# Диапазоны значений параметров
PARAM_RANGES = {
    'budget': (100_000, 10_000_000),
    'duration': (1, 24),
    'novelty': (0, 2),
    'experience': (0, 10),
    'contractors': (0, 100),
    'risk_plan': (0, 10),
    'time_buffer': (0, 30),
    'cost_buffer': (0, 30)
}

PARAM_NAMES = list(PARAM_RANGES.keys())

def random_solution():
    """Генерирует один случайный набор параметров проекта."""
    return {
        key: random.randint(*PARAM_RANGES[key]) for key in PARAM_NAMES
    }

def update_position(wolf, alpha, beta, delta, a=0.5):
    """Обновляет параметры волка на основе α, β и δ."""
    new_wolf = {}
    for key in PARAM_NAMES:
        A = random.uniform(-a, a)
        C = random.uniform(0, 2)

        D_alpha = abs(C * alpha[key] - wolf[key])
        D_beta = abs(C * beta[key] - wolf[key])
        D_delta = abs(C * delta[key] - wolf[key])

        X1 = alpha[key] - A * D_alpha
        X2 = beta[key] - A * D_beta
        X3 = delta[key] - A * D_delta

        new_value = (X1 + X2 + X3) / 3

        # Приведение в допустимые границы
        min_val, max_val = PARAM_RANGES[key]
        new_value = max(min_val, min(max_val, new_value))

        # Округляем до int (можно сделать более гибко)
        new_wolf[key] = int(round(new_value))

    return new_wolf

def gwo_optimize(n_wolves=20, n_iter=20):
    """Основной цикл GWO. Возвращает лучшее решение (альфа) и его RiskScore."""
    wolves = [random_solution() for _ in range(n_wolves)]

    for iteration in range(n_iter):
        wolves.sort(key=calculate_risk_score)
        alpha, beta, delta = wolves[0], wolves[1], wolves[2]

        new_wolves = []
        for i in range(3, n_wolves):
            new_wolf = update_position(wolves[i], alpha, beta, delta)
            new_wolves.append(new_wolf)

        wolves[3:] = new_wolves  # заменяем только омег

    best = wolves[0]
    return {
        'best_solution': best,
        'min_risk_score': calculate_risk_score(best)
    }
