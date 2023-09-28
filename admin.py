from django.contrib import admin
from .models import Docente, Curso, DeclaracaoEmitida, export_to_excel, export_cursos_to_excel
from django.contrib import admin
from openpyxl import Workbook
from django.urls import reverse
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponse


admin.site.site_header = 'Painel Administrativo'
admin.site.register(DeclaracaoEmitida)



@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'matricula', 'nome', 'endereco', 'telefone', 'rg', 'data_nascimento', 'filiacao', 'naturalidade', 'email', 'formacao_academica', 'pis_pasep', 'dados_bancarios', 'avaliacao', 'observacao']
    list_editable = ['endereco', 'telefone', 'email', 'observacao']
    list_filter = ['avaliacao']
    search_fields = ['cpf', 'matricula', 'nome', 'email']
    actions = [export_to_excel]

    def export_to_excel_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Exportar para Excel</a>',
            reverse('export_to_excel')
        )
    export_to_excel_button.short_description = "Exportar para Excel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export_to_excel/', self.export_to_excel_view, name='export_to_excel'),
        ]
        return custom_urls + urls

    def export_to_excel_view(self, request):
        docentes = self.get_queryset(request)
        response = export_to_excel(self, request, docentes)
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_to_excel_url'] = reverse('admin:export_to_excel')
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'docente', 'turma', 'ano', 'componente', 'perfil', 'carga_horaria', 'periodo']
    list_filter = ['docente', 'ano', 'periodo']
    search_fields = ['nome', 'docente__nome']
    actions = [export_cursos_to_excel]

    def export_cursos_to_excel_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Exportar para Excel</a>',
            reverse('export_cursos_to_excel')
        )
    export_cursos_to_excel_button.short_description = "Exportar para Excel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export_cursos_to_excel/', self.export_cursos_to_excel_view, name='export_cursos_to_excel'),
        ]
        return custom_urls + urls

    def export_cursos_to_excel_view(self, request):
        cursos = self.get_queryset(request)
        response = export_cursos_to_excel(self, request, cursos)
        return response

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_cursos_to_excel_url'] = reverse('admin:export_cursos_to_excel')
        return super().changelist_view(request, extra_context=extra_context)
