from django.conf.urls import include
from .models import Especialidade, Medico, Agenda, Hora
from .serializers import MedicoSerializer, EspecialidadeSerializer, \
    AgendaSerializer, ConsultaListSerializer, ConsultaCreateSerializer
from rest_framework import generics
from django.utils.timezone import now
from datetime import datetime
from .mixins import ReadWriteSerializerMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class EspecialidadeList(generics.ListCreateAPIView):
    serializer_class = EspecialidadeSerializer

    def get_queryset(self):
        queryset = Especialidade.objects.all()

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(nome__icontains=search)

        return queryset


class MedicoList(generics.ListCreateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

    def get_queryset(self):
        queryset = Medico.objects.all()

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(nome__icontains=search)

        especialidade = self.request.query_params.getlist(
            'especialidade', None)

        if especialidade:
            queryset = queryset.filter(especialidade__id__in=especialidade)

        return queryset


class AgendaList(generics.ListCreateAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def get_queryset(self):
        queryset = Agenda.objects.filter(dia__gte=now())
        queryset = queryset.filter(horarios_agendamento__paciente__isnull=True)

        data_inicio = self.request.query_params.get('data_inicio', None)
        data_final = self.request.query_params.get('data_final', None)

        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            queryset = queryset.filter(dia__gte=data_inicio)

        if data_final:
            data_final = datetime.strptime(data_final, "%Y-%m-%d")
            queryset = queryset.filter(dia__lte=data_final)

        especialidade = self.request.query_params.getlist(
            'especialidade', None)

        medico = self.request.query_params.getlist(
            'medico', None)

        if especialidade:
            queryset = queryset.filter(
                medico__especialidade__id__in=especialidade)

        if medico:
            queryset = queryset.filter(medico__id__in=especialidade)

        return queryset.distinct()


class ConsultaList(generics.ListCreateAPIView):
    read_serializer_class = ConsultaListSerializer
    write_serializer_class = ConsultaCreateSerializer

    def get_queryset(self):
        queryset = Hora.objects.filter(paciente=self.request.user)

        queryset = queryset.filter(agenda__dia__gte=now())

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hora = serializer.save()
        hora.paciente = request.user
        hora.save()

        headers = self.get_success_headers(serializer.data)
        return Response(self.read_serializer_class(hora).data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.write_serializer_class

        return self.read_serializer_class


class ConsultaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hora.objects.filter(agenda__dia__gte=now())
    serializer_class = ConsultaListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.paciente = None
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
