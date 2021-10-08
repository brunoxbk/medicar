from rest_framework import serializers
from .models import Especialidade, Medico, Agenda, Consulta
from django.utils.timezone import now
from datetime import datetime
from django.db.models import Case, Value, When, OuterRef, CharField


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ['id', 'nome', ]


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer(many=False)

    class Meta:
        model = Medico
        fields = ['id', 'nome', 'crm', 'especialidade']


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ['order', 'title', 'duration']


class AgendaSerializer(serializers.ModelSerializer):
    horarios = serializers.SerializerMethodField()

    def get_horarios(self, obj):

        horarios = obj.consultas_agendamento\
            .filter(paciente__isnull=True)

        if obj.dia == now().date():
            horarios = horarios.filter(hora__gt=datetime.now().time())

        return horarios.values_list('hora', flat=True)

    class Meta:
        model = Agenda
        fields = ['id', 'dia', 'medico', 'horarios']


class ConsultaListSerializer(serializers.ModelSerializer):
    dia = serializers.SerializerMethodField()
    medico = MedicoSerializer()

    def get_dia(self, obj):
        return obj.agenda.dia

    class Meta:
        model = Consulta
        fields = ['id', 'hora', 'dia', 'medico']


class ConsultaCreateSerializer(serializers.ModelSerializer):
    hora = serializers.TimeField(
        input_formats=["%H:%M:%S", ])

    class Meta:
        model = Consulta
        fields = ['hora', 'agenda']

    def validate(self, data):

        agenda = data['agenda']

        if agenda.dia < datetime.now().date():
            raise serializers.ValidationError("Agenda inválida")

        hora = Consulta.objects.filter(
            hora=data['hora'], agenda=agenda, paciente__isnull=True).last()
        if not hora:
            raise serializers.ValidationError("Horário inválido")

        return data

    def create(self, validated_data):
        hora = Consulta.objects.filter(
            hora=validated_data['hora'], agenda=validated_data['agenda'], paciente__isnull=True).last()
        return hora
