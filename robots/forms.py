from django import forms


class ProductionReportForm(forms.Form):
    start_date = forms.DateField(
        label='Дата начала',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    end_date = forms.DateField(
        label='Дата окончания',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
