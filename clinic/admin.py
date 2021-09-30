from django.contrib import admin
from .models import Medico, Agenda, Especialidade, Hora


class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome',)
    search_fields = ('nome', )
    exclude = ('apagado_em',)


class MedicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'crm', 'especialidade')
    list_filter = ('especialidade',)
    search_fields = ('nome', )
    exclude = ('apagado_em',)


class HoraInline(admin.StackedInline):
    model = Hora
    exclude = ('apagado_em',)
    extra = 0


class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'dia', 'medico')
    list_filter = ('medico__especialidade', 'medico')
    search_fields = ('medico__nome',  'medico__especialidade__nome')
    exclude = ('apagado_em',)
    inlines = [HoraInline, ]


admin.site.register(Especialidade, EspecialidadeAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Agenda, AgendaAdmin)
