# Generated by Django 3.2.7 on 2021-09-29 21:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='alterado em')),
                ('apagado_em', models.DateTimeField(blank=True, null=True, verbose_name='deletado em')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('dia', models.DateField(verbose_name='dia')),
            ],
            options={
                'verbose_name': 'agendas',
                'verbose_name_plural': 'agendas',
            },
        ),
        migrations.CreateModel(
            name='Especialidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='alterado em')),
                ('apagado_em', models.DateTimeField(blank=True, null=True, verbose_name='deletado em')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('nome', models.CharField(max_length=100, verbose_name='nome')),
            ],
            options={
                'verbose_name': 'especialidade',
                'verbose_name_plural': 'especialidades',
            },
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='alterado em')),
                ('apagado_em', models.DateTimeField(blank=True, null=True, verbose_name='deletado em')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('nome', models.CharField(max_length=120, verbose_name='nome')),
                ('crm', models.IntegerField(verbose_name='CRM')),
                ('email', models.EmailField(max_length=100, verbose_name='e-mail')),
                ('telefone', models.CharField(max_length=120, verbose_name='telefone')),
                ('especialidade', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='medicos', to='clinic.especialidade', verbose_name='especialidade')),
            ],
            options={
                'verbose_name': 'médico',
                'verbose_name_plural': 'médicos',
            },
        ),
        migrations.CreateModel(
            name='Hora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='alterado em')),
                ('apagado_em', models.DateTimeField(blank=True, null=True, verbose_name='deletado em')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('hora', models.TimeField(choices=[(datetime.time(8, 0), '08:00'), (datetime.time(9, 0), '09:00'), (datetime.time(10, 0), '10:00'), (datetime.time(11, 0), '11:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00')], verbose_name='hora')),
                ('agenda', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='horarios_agendamento', to='clinic.agenda', verbose_name='agenda')),
                ('paciente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='agendamentos_paciente', to=settings.AUTH_USER_MODEL, verbose_name='paciente')),
            ],
            options={
                'verbose_name': 'horário',
                'verbose_name_plural': 'horários',
            },
        ),
        migrations.AddField(
            model_name='agenda',
            name='medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='agendas_medico', to='clinic.medico', verbose_name='médico'),
        ),
    ]
