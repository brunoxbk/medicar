from django import forms
from .models import Agenda, Medico
from datetime import datetime


class AgendaForm(forms.ModelForm):

    def clean(self):
        dia = self.cleaned_data['dia']
        medico = self.cleaned_data['medico']

        if dia < datetime.now().date():
            raise forms.ValidationError("A data não pode ser anterior a hoje")

        agendas = Agenda.objects.filter(medico=medico, dia=dia).exists()

        if agendas:
            raise forms.ValidationError(
                "Não é possivel duas agendas para o mesmo médico no mesmo dia")

        return self.cleaned_data

    class Meta:
        model = Agenda
        fields = ['dia', 'medico']
