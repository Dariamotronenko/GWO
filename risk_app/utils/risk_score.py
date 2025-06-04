def normalize(value, min_val, max_val, reverse=False):
    """
    Нормализует значение в диапазон [0, 1].
    reverse=True — инвертирует (чем больше значение, тем ниже риск).
    """
    norm = (value - min_val) / (max_val - min_val)
    return 1 - norm if reverse else norm


def calculate_risk_score(data):
    weights = {
        'budget': 0.15,
        'duration': 0.10,
        'novelty': 0.10,
        'experience': 0.10,
        'contractors': 0.15,
        'risk_plan': 0.20,
        'time_buffer': 0.10,
        'cost_buffer': 0.10,
    }

    # Явно преобразуем значения к числам
    budget = int(data['budget'])
    duration = int(data['duration'])
    novelty = int(data['novelty'])  # если из ChoiceField — это строка
    experience = int(data['experience'])
    contractors = int(data['contractors'])
    risk_plan = int(data['risk_plan'])
    time_buffer = int(data['time_buffer'])
    cost_buffer = int(data['cost_buffer'])

    # Нормализация
    norm_budget = normalize(budget, 100_000, 10_000_000)
    norm_duration = normalize(duration, 1, 24)
    norm_novelty = normalize(novelty, 0, 2)
    norm_experience = 1 - normalize(experience, 0, 10)
    norm_contractors = normalize(contractors, 0, 100)
    norm_risk_plan = 1 - normalize(risk_plan, 0, 10)
    norm_time_buffer = 1 - normalize(time_buffer, 0, 30)
    norm_cost_buffer = 1 - normalize(cost_buffer, 0, 30)

    total_score = (
        weights['budget'] * norm_budget +
        weights['duration'] * norm_duration +
        weights['novelty'] * norm_novelty +
        weights['experience'] * norm_experience +
        weights['contractors'] * norm_contractors +
        weights['risk_plan'] * norm_risk_plan +
        weights['time_buffer'] * norm_time_buffer +
        weights['cost_buffer'] * norm_cost_buffer
    )

    return round(total_score, 4)


