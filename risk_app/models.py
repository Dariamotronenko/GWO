from django.db import models

class RiskEvaluation(models.Model):
    # Параметры проекта
    budget = models.IntegerField(verbose_name="Бюджет проекта (₽)")
    duration = models.IntegerField(verbose_name="Сроки реализации (мес)")
    novelty = models.IntegerField(verbose_name="Новизна проекта")  # 0 / 1 / 2
    experience = models.IntegerField(verbose_name="Опыт менеджера (лет)")
    contractors = models.IntegerField(verbose_name="Доля подрядчиков (%)")
    risk_plan = models.IntegerField(verbose_name="Развитость плана управления рисками (0–10)")
    time_buffer = models.IntegerField(verbose_name="Запас по срокам (%)")
    cost_buffer = models.IntegerField(verbose_name="Запас по бюджету (%)")

    # Расчёты
    user_score = models.FloatField(verbose_name="RiskScore до оптимизации")
    optimized_score = models.FloatField(verbose_name="RiskScore после GWO")

    # Временная метка
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Оценка риска проекта"
        verbose_name_plural = "Оценки рисков проектов"

    def __str__(self):
        return f"Проект от {self.created_at.strftime('%d.%m.%Y %H:%M')} — Score: {self.user_score:.2f}"
