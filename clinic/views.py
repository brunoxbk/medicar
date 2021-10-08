from django.conf.urls import include
from .models import Especialidade, Medico, Agenda, Consulta
from .serializers import MedicoSerializer, EspecialidadeSerializer, \
    AgendaSerializer, ConsultaListSerializer, ConsultaCreateSerializer
from rest_framework import generics
from django.utils.timezone import now
from .mixins import ReadWriteSerializerMixin
from rest_framework.response import Response
from rest_framework import status
from .filters import FiltroMedico, FiltroEspecialidade, FiltroAgenda


class EspecialidadeList(generics.ListCreateAPIView):
    serializer_class = EspecialidadeSerializer
    queryset = Especialidade.objects.all()
    filterset_class = FiltroEspecialidade


class MedicoList(generics.ListCreateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filterset_class = FiltroMedico


class AgendaList(generics.ListCreateAPIView):
    queryset = Agenda.objects.filter(
        dia__gte=now(), consultas_agendamento__paciente__isnull=True).distinct()
    serializer_class = AgendaSerializer
    filterset_class = FiltroAgenda


class ConsultaList(ReadWriteSerializerMixin, generics.ListCreateAPIView):
    read_serializer_class = ConsultaListSerializer
    write_serializer_class = ConsultaCreateSerializer

    def get_queryset(self):
        queryset = Consulta.objects.filter(paciente=self.request.user)

        queryset = queryset.filter(agenda__dia__gte=now())

        return queryset

    def perform_create(self, serializer):
        consulta = serializer.save()
        consulta.paciente = self.request.user
        consulta.save()

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     consulta = serializer.save()
    #     consulta.paciente = request.user
    #     consulta.save()

    #     headers = self.get_success_headers(serializer.data)
    #     return Response(self.read_serializer_class(consulta).data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.write_serializer_class

        return self.read_serializer_class


class ConsultaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consulta.objects.filter(agenda__dia__gte=now())
    serializer_class = ConsultaListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.paciente = None
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
