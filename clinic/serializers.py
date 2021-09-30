from rest_framework import serializers
from .models import Especialidade, Medico, Agenda, Hora
from django.utils.timezone import now
from datetime import datetime


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ['id', 'nome', ]


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer(many=False)

    class Meta:
        model = Medico
        fields = ['id', 'nome', 'crm', 'especialidade']


class HoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hora
        fields = ['order', 'title', 'duration']


class AgendaSerializer(serializers.ModelSerializer):
    horarios = serializers.SerializerMethodField()

    def get_horarios(self, obj):
        # .filter(hora__gte=datetime.now().time())\
        return obj.horarios_agendamento\
            .filter(paciente__isnull=True)\
            .values_list('hora', flat=True)

    class Meta:
        model = Agenda
        fields = ['id', 'dia', 'medico', 'horarios']


class ConsultaListSerializer(serializers.ModelSerializer):
    dia = serializers.SerializerMethodField()
    medico = MedicoSerializer()

    def get_dia(self, obj):
        return obj.agenda.dia

    # def get_medico(self, obj):
    #     return MedicoSerializer(obj.agenda.medico)

    class Meta:
        model = Hora
        fields = ['id', 'hora', 'dia', 'medico']


class ConsultaCreateSerializer(serializers.ModelSerializer):
    hora = serializers.TimeField(
        input_formats=["%H:%M:%S", ])

    class Meta:
        model = Hora
        fields = ['hora', 'agenda']

    def validate(self, data):
        hora = Hora.objects.filter(
            hora=data['hora'], agenda=data['agenda'], paciente__isnull=True).last()
        if not hora:
            raise serializers.ValidationError("Horário inválido")

        return data

    def create(self, validated_data):
        print(validated_data)
        hora = Hora.objects.filter(
            hora=validated_data['hora'], agenda=validated_data['agenda'], paciente__isnull=True).last()
        return hora
