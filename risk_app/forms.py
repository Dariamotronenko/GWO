from django import forms
from django.core.exceptions import ValidationError

class ProjectForm(forms.Form):
    budget = forms.IntegerField(
        label="Бюджет проекта (₽)",
        min_value=100_000,
        max_value=10_000_000,
        initial=1_000_000,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    duration = forms.IntegerField(
        label="Сроки реализации (мес)",
        min_value=1,
        max_value=24,
        initial=12,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    novelty = forms.TypedChoiceField(
        label="Новизна проекта",
        choices=[
            (0, "Типовой"),
            (1, "Новый"),
            (2, "Инновационный")
        ],
        initial=1,
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    experience = forms.IntegerField(
        label="Опыт менеджера (лет)",
        min_value=0,
        max_value=10,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    contractors = forms.IntegerField(
        label="Доля подрядчиков (%)",
        min_value=0,
        max_value=100,
        initial=30,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    risk_plan = forms.IntegerField(
        label="Развитость плана управления рисками (0–10)",
        min_value=0,
        max_value=10,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'data-bs-toggle': 'modal',
            'data-bs-target': '#riskPlanModal',
            'aria-describedby': 'riskPlanHelp'
        })
    )

    time_buffer = forms.IntegerField(
        label="Запас по срокам (%)",
        min_value=0,
        max_value=30,
        initial=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    cost_buffer = forms.IntegerField(
        label="Запас по бюджету (%)",
        min_value=0,
        max_value=30,
        initial=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget and budget < 100_000:
            raise ValidationError('Бюджет проекта не может быть меньше 100,000 ₽')
        return budget

    def clean_contractors(self):
        contractors = self.cleaned_data.get('contractors')
        if contractors and contractors > 100:
            raise ValidationError('Доля подрядчиков не может превышать 100%')
        return contractors

    def clean_risk_plan(self):
        risk_plan = self.cleaned_data.get('risk_plan')
        if risk_plan and (risk_plan < 0 or risk_plan > 10):
            raise ValidationError('Оценка плана управления рисками должна быть от 0 до 10')
        return risk_plan
