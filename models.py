from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime
from django.http import HttpResponse
from openpyxl import Workbook


class Docente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    rg = models.CharField(max_length=20)
    filiacao = models.CharField(max_length=200)
    naturalidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Telefone deve estar no formato (xx) xxxxx-xxxx'
            )
        ]
    )
    email = models.EmailField()
    matricula = models.CharField(max_length=20)
    formacao_academica = models.CharField(max_length=200)
    pis_pasep = models.CharField(max_length=20)
    dados_bancarios = models.CharField(max_length=200)
    avaliacao = models.CharField(max_length=200, blank=True, null=True)
    observacao = models.CharField(max_length=200, blank=True, null=True)

    def clean(self):
        cpf_validator = RegexValidator(
            regex=r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$',
            message='CPF deve estar no formato xxx.xxx.xxx-xx'
        )
        data_nascimento_validator = RegexValidator(
            regex=r'^\d{2}/\d{2}/\d{4}$',
            message='Data de nascimento deve estar no formato DD/MM/YYYY'
        )

        # Validação e formatação do CPF
        if self.cpf:
            cpf = self.cpf.replace('.', '').replace('-', '')
            try:
                cpf_validator(cpf)
            except ValidationError:
                raise ValidationError({'cpf': cpf_validator.message})
            self.cpf = cpf

        # Validação e formatação da data de nascimento
        if self.data_nascimento:
            data_nascimento = self.data_nascimento.strftime('%d/%m/%Y')
            try:
                data_nascimento_validator(data_nascimento)
            except ValidationError:
                raise ValidationError(
                    {'data_nascimento': data_nascimento_validator.message})
            self.data_nascimento = datetime.strptime(
                data_nascimento, '%d/%m/%Y')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name='cursos')
    turma = models.CharField(max_length=100)
    ano = models.IntegerField()
    componente = models.CharField(max_length=100)
    perfil = models.CharField(max_length=100)
    carga_horaria = models.IntegerField(default=0)
    periodo = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Turma(models.Model):
    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, related_name='turmas')
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return f"{self.curso} - Turma {self.id}"


class CustomUser(AbstractUser):
    # Adicione campos personalizados, se necessário

    class Meta(AbstractUser.Meta):
        # Defina um related_name exclusivo para o campo 'groups'
        db_table = 'custom_user'

    groups = models.ManyToManyField(
        Group, verbose_name='groups', blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        help_text='Specific permissions for this user.',
        related_query_name='custom_user'
    )


def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=docentes.xlsx'

    workbook = Workbook()
    worksheet = workbook.active

    # Cabeçalhos das colunas
    headers = ['CPF', 'Matrícula', 'Nome', 'Endereço', 'Telefone', 'RG', 'Data de Nascimento', 'Filiação',
               'Naturalidade', 'Email', 'Formação Acadêmica', 'PIS/PASEP', 'Dados Bancários', 'Avaliação', 'Observação']
    worksheet.append(headers)

    # Dados dos docentes
    for docente in queryset:
        row = [docente.cpf, docente.matricula, docente.nome, docente.endereco, docente.telefone, docente.rg, docente.data_nascimento, docente.filiacao,
               docente.naturalidade, docente.email, docente.formacao_academica, docente.pis_pasep, docente.dados_bancarios, docente.avaliacao, docente.observacao]
        worksheet.append(row)

    workbook.save(response)
    return response


export_to_excel.short_description = "Exportar para Excel"


def export_cursos_to_excel(modeladmin, request, queryset):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=cursos.xlsx'

    workbook = Workbook()
    worksheet = workbook.active

    # Cabeçalhos das colunas
    headers = ['Nome', 'Docente', 'Turma', 'Ano',
               'Componente', 'Perfil', 'Carga Horária', 'Período']
    worksheet.append(headers)

    # Dados dos cursos
    for curso in queryset:
        row = [
            curso.nome,
            str(curso.docente),  # Converter o objeto Docente em uma string
            curso.turma,
            curso.ano,
            curso.componente,
            curso.perfil,
            curso.carga_horaria,
            curso.periodo
        ]
        worksheet.append(row)

    workbook.save(response)
    return response


export_cursos_to_excel.short_description = "Exportar para Excel"

from django.db import models
from django.core.validators import RegexValidator

from django.db import models

class Servidor(models.Model):
    SETORES = (
        ('Direção', 'Direção'),
        ('Biblioteca', 'Biblioteca'),
        ('Sec Escolar', 'Sec Escolar'),
        ('NGTES', 'NGTES'),
        ('Equipe Técnica', 'Equipe Técnica'),
        ('Núcleo de TI', 'Núcleo de TI'),
        ('úcleo Pedagógico', 'Núcleo Pedagógico'),
        ('Núcleo de REsidências', 'Núcleo de Residências'),
    )
    setor = models.CharField(max_length=30, choices=SETORES)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    rg = models.CharField(max_length=20)
    filiacao = models.CharField(max_length=200)
    naturalidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Telefone deve estar no formato (xx) xxxxx-xxxx'
            )
        ]
    )
    email = models.EmailField()
    matricula = models.CharField(max_length=20)
    formacao_academica = models.CharField(max_length=200)
    pis_pasep = models.CharField(max_length=20)
    dados_bancarios = models.CharField(max_length=200)
    avaliacao = models.CharField(max_length=200, blank=True, null=True)
    observacao = models.CharField(max_length=200, blank=True, null=True)

    def clean(self):
        cpf_validator = RegexValidator(
            regex=r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$',
            message='CPF deve estar no formato xxx.xxx.xxx-xx'
        )
        data_nascimento_validator = RegexValidator(
            regex=r'^\d{2}/\d{2}/\d{4}$',
            message='Data de nascimento deve estar no formato DD/MM/YYYY'
        )

        # Validação e formatação do CPF
        if self.cpf:
            cpf = self.cpf.replace('.', '').replace('-', '')
            try:
                cpf_validator(cpf)
            except ValidationError:
                raise ValidationError({'cpf': cpf_validator.message})
            self.cpf = cpf

        # Validação e formatação da data de nascimento
        if self.data_nascimento:
            data_nascimento = self.data_nascimento.strftime('%d/%m/%Y')
            try:
                data_nascimento_validator(data_nascimento)
            except ValidationError:
                raise ValidationError(
                    {'data_nascimento': data_nascimento_validator.message})
            self.data_nascimento = datetime.strptime(
                data_nascimento, '%d/%m/%Y')

    def __str__(self):
        return self.nome

from django.db import models

class Documento(models.Model):
    TIPOS_DOCUMENTO = (
        ('graduacao', 'Graduação'),
        ('especializacao', 'Especialização'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
    )

    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE, editable=False)
    tipo = models.CharField(max_length=20, choices=TIPOS_DOCUMENTO)
    arquivo = models.FileField(upload_to='documentos/')

    def __str__(self):
        return f"{self.servidor.nome} - {self.tipo}"
