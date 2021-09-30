from django.db import models
from django.contrib.auth.models import User
import datetime


class SuperClass(models.Model):
    class Meta:
        abstract = True
        ordering = ('-criado_em',)

    criado_em = models.DateTimeField('criado em', auto_now_add=True)
    alterado_em = models.DateTimeField('alterado em', auto_now=True)
    apagado_em = models.DateTimeField('deletado em', null=True, blank=True)
    ativo = models.BooleanField('ativo', default=True)


class Especialidade(SuperClass):
    '''
        Deve ser possível cadastrar as especialidades médicas (ex: CARDIOLOGIA, PEDIATRIA)
        que a clínica atende fornecendo as seguintes informações:
        Nome: nome da especialidade médica (obrigatório)
    '''
    nome = models.CharField(verbose_name='nome', max_length=100)

    class Meta:
        verbose_name = 'especialidade'
        verbose_name_plural = 'especialidades'

    def __str__(self):
        return self.nome


class Medico(SuperClass):
    '''
        Deve ser possível cadastrar os médicos que podem atender na clínica fornecendo as seguintes informações:

        Nome: Nome do médico (obrigatório)
        CRM: Número do médico no conselho regional de medicina (obrigatório)
        E-mail: Endereço de e-mail do médico
        Telefone: Telefone do médico
        Especialidade: Especialidade na qual o médico atende
    '''
    nome = models.CharField(verbose_name='nome', max_length=120)
    crm = models.IntegerField(verbose_name='CRM')
    email = models.EmailField(verbose_name='e-mail', max_length=100)
    telefone = models.CharField(verbose_name='telefone', max_length=120)

    especialidade = models.ForeignKey(
        Especialidade, verbose_name='especialidade',
        on_delete=models.DO_NOTHING,
        related_name="medicos")

    class Meta:
        verbose_name = 'médico'
        verbose_name_plural = 'médicos'

    def __str__(self):
        return self.nome


class Agenda(SuperClass):
    '''
        Deve ser possível criar uma agenda para um médico em um dia específico fornecendo as seguintes informações:

        Médico: Médico que será alocado (obrigatório)
        Dia: Data de alocação do médico (obrigatório)
        Horários: Lista de horários na qual o médico deverá ser alocado para o dia especificado (obrigatório)

        Não deve ser possível criar mais de uma agenda para um médico em um mesmo dia
        Não deve ser possível criar uma agenda para um médico em um dia passado
    '''

    dia = models.DateField('dia')
    medico = models.ForeignKey(
        Medico, verbose_name='médico',
        on_delete=models.DO_NOTHING,
        related_name="agendas_medico")

    class Meta:
        verbose_name = 'agendas'
        verbose_name_plural = 'agendas'
        ordering = ('dia',)

    def __str__(self):
        return str(self.pk)


class Hora(SuperClass):
    class HourChoices(datetime.time, models.Choices):
        HOUR_08 = 8, 0, 0, '08:00'
        HOUR_09 = 9, 0, 0, '09:00'
        HOUR_10 = 10, 0, 0, '10:00'
        HOUR_11 = 11, 0, 0, '11:00'
        HOUR_14 = 14, 0, 0, '14:00'
        HOUR_15 = 15, 0, 0, '15:00'
        HOUR_16 = 16, 0, 0, '16:00'
        HOUR_17 = 17, 0, 0, '17:00'

    agenda = models.ForeignKey(
        Agenda, verbose_name='agenda',
        on_delete=models.DO_NOTHING,
        related_name="horarios_agendamento")
    hora = models.TimeField(
        'hora', choices=HourChoices.choices)
    paciente = models.ForeignKey(
        User, verbose_name='paciente',
        on_delete=models.DO_NOTHING, null=True, blank=True,
        related_name="agendamentos_paciente")

    @property
    def medico(self):
        return self.agenda.medico

    class Meta:
        verbose_name = 'horário'
        verbose_name_plural = 'horários'
        ordering = ('hora',)

    def __str__(self):
        return str(self.pk)
