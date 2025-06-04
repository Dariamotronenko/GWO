from django.shortcuts import render
from .forms import ProjectForm
from .utils.risk_score import calculate_risk_score
from .utils.gwo import gwo_optimize
from .models import RiskEvaluation

def interpret_risk(score):
    """Возвращает категорию риска по числовому значению RiskScore."""
    if score <= 0.20:
        return "🟦 Очень низкий риск"
    elif score <= 0.40:
        return "🟢 Низкий риск"
    elif score <= 0.60:
        return "🟡 Умеренный риск"
    elif score <= 0.80:
        return "🟠 Высокий риск"
    else:
        return "🔴 Критический риск"

def index(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # Данные, введённые пользователем
            user_data = form.cleaned_data
            user_score = calculate_risk_score(user_data)

            # Оптимизация параметров с помощью GWO
            optimized = gwo_optimize()
            optimized_score = optimized['min_risk_score']

            # Сохраняем результаты в базу данных
            RiskEvaluation.objects.create(
                budget=user_data['budget'],
                duration=user_data['duration'],
                novelty=user_data['novelty'],
                experience=user_data['experience'],
                contractors=user_data['contractors'],
                risk_plan=user_data['risk_plan'],
                time_buffer=user_data['time_buffer'],
                cost_buffer=user_data['cost_buffer'],
                user_score=user_score,
                optimized_score=optimized_score
            )

            return render(request, 'risk_app/result.html', {
                'form_data': user_data,
                'user_score': user_score,
                'risk_category': interpret_risk(user_score),
                'optimized_score': optimized_score,
                'optimized_values': optimized['best_solution'],
                'optimized_category': interpret_risk(optimized_score)
            })
    else:
        form = ProjectForm()

    return render(request, 'risk_app/form.html', {'form': form})