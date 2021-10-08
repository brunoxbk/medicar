from django.db.models.query import QuerySet
import django_filters
from .models import Especialidade, Medico


class FiltroEspecialidade(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="nome", lookup_expr="icontains")


class FiltroMedico(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="nome", lookup_expr="icontains")
    especialidade = django_filters.ModelMultipleChoiceFilter(
        field_name='especialidade__pk', to_field_name="pk", queryset=Especialidade.objects.all())


class FiltroAgenda(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="nome", lookup_expr="icontains")
    medico = django_filters.ModelMultipleChoiceFilter(
        field_name='medico__pk', to_field_name="pk",
        queryset=Medico.objects.all())
    especialidade = django_filters.ModelMultipleChoiceFilter(
        field_name='medico__especialidade__pk', to_field_name="pk",
        queryset=Medico.objects.all())
    # medico__especialidade = django_filters.AllValuesMultipleFilter(
    #     field_name="medico__especialidade", label="especialidade", distinct=True)
    data_inicio = django_filters.DateTimeFilter(
        field_name="dia", lookup_expr="gte")
    data_final = django_filters.DateTimeFilter(
        field_name="dia", lookup_expr="lte")
