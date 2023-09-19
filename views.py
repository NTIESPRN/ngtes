from django.shortcuts import render, redirect
from .models import Docente, Curso, Servidor, Documento
from .forms import DocenteForm, CursoForm, ServidorForm, DeclaracaoForm
from django.http import FileResponse
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect


import re

def format_data_nascimento(data):
    # Formata a data de nascimento no formato DD/MM/YYYY
    return data.strftime('%d/%m/%Y')

def format_cpf(cpf):
    # Remove caracteres não numéricos e formata o CPF no formato XXX.XXX.XXX-XX
    cpf = re.sub('[^0-9]', '', cpf)
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

def format_telefone(telefone):
    # Remove caracteres não numéricos e formata o telefone no formato (XX) XXXXX-XXXX
    telefone = re.sub('[^0-9]', '', telefone)
    return f'({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}'



@login_required
def cadastro_docente(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['data_nascimento'] = format_data_nascimento(cleaned_data['data_nascimento'])
            cleaned_data['cpf'] = format_cpf(cleaned_data['cpf'])
            cleaned_data['telefone'] = format_telefone(cleaned_data['telefone'])
            form.save()
            return redirect('cadastro_docente')
    else:
        form = DocenteForm()
    
    cursos = Curso.objects.all()  # Obtenha todos os cursos do banco de dados
    docentes = Docente.objects.all()  # Obtenha todos os docentes do banco de dados

    return render(request, 'cadastro_docente.html', {'form': form, 'cursos': cursos, 'docentes': docentes})




@login_required
def cadastro_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastro_curso')
    else:
        form = CursoForm()

    cursos = Curso.objects.all()  # Obtenha todos os cursos do banco de dados
    docentes = Docente.objects.order_by('nome')  # Obtenha todos os docentes do banco de dados

    return render(request, 'cadastro_curso.html', {'form': form, 'cursos': cursos, 'docentes': docentes})







def busca(request):
    cursos = Curso.objects.all()
    docentes = Docente.objects.all()

    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        docente_id = request.POST.get('docente_id')

        if curso_id:
            cursos = cursos.filter(id=curso_id)
        
        if docente_id:
            cursos = cursos.filter(docente__id=docente_id)

        if 'export_excel' in request.POST:
            filename = export_to_excel(cursos)
            response = FileResponse(open(filename, 'rb'), as_attachment=True, filename='cursos.xlsx')
            return response

    return render(request, 'busca.html', {'cursos': cursos, 'docentes': docentes})

from django.http import FileResponse

def export_to_excel(cursos):
    cursos = Curso.objects.all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    headers = ['Nome', 'Docente', 'Turma', 'Ano', 'Componente', 'Perfil', 'Carga Horária', 'Período']
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        cell = sheet[f'{col_letter}1']
        cell.value = header
        cell.font = openpyxl.styles.Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    for row_num, curso in enumerate(cursos, 2):
        sheet[f'A{row_num}'] = curso.nome
        if curso.docente:
            sheet[f'B{row_num}'] = curso.docente.nome
        else:
            sheet[f'B{row_num}'] = ""
        sheet[f'C{row_num}'] = curso.turma
        sheet[f'D{row_num}'] = curso.ano
        sheet[f'E{row_num}'] = curso.componente
        sheet[f'F{row_num}'] = curso.perfil
        sheet[f'G{row_num}'] = curso.carga_horaria
        sheet[f'H{row_num}'] = curso.periodo

    for col_num in range(1, len(headers) + 1):
        col_letter = get_column_letter(col_num)
        sheet.column_dimensions[col_letter].width = 15

    filename = 'cursos.xlsx'
    workbook.save(filename)
    response = FileResponse(open(filename, 'rb'), as_attachment=True, filename='cursos.xlsx')
    return response



from django.db.models import Q

@login_required
def index(request):
    query = request.POST.get('query', '')

    if query == '.':
        cursos = Curso.objects.all()
    else:
        cursos = Curso.objects.filter(Q(nome__icontains=query) | Q(docente__nome__icontains=query))

    return render(request, 'index.html', {'cursos': cursos})


def perfil_docente(request, docente_id):
    # Lógica para obter os detalhes do docente com base no 'docente_id'
    # ...
    docente = Docente.objects.get(id=docente_id)
    
    return render(request, 'perfil_docente.html', {'docente': docente})
# views.py (do aplicativo)
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST,instance=curso)
        if form.is_valid():
            form.save()
            return redirect('cadastro_curso')
    else:
        form = CursoForm(instance=curso)

    cursos = Curso.objects.all()  # Obtenha todos os cursos do banco de dados
    docentes = Docente.objects.all()  # Obtenha todos os docentes do banco de dados

    return render(request, 'cadastro_curso.html', {'form': form, 'cursos': cursos, 'docentes': docentes})

def editar_docente(request, pk):
    docentes = get_object_or_404(Docente, pk=pk)
    if request.method == 'POST':
        form = DocenteForm(request.POST,instance=docentes)
        if form.is_valid():
            form.save()
            return redirect('cadastro_docente')
    else:
        form = DocenteForm(instance=docentes)

    cursos = Curso.objects.all()  # Obtenha todos os cursos do banco de dados
    docentes = Docente.objects.all()  # Obtenha todos os docentes do banco de dados

    return render(request, 'cadastro_docente.html', {'form': form, 'cursos': cursos, 'docentes': docentes})


from django.db.models import Q

def cadastro_servidor(request):
    sort_field = request.GET.get('sort')  # Obtém o parâmetro "sort" da URL

    if request.method == 'POST':
        form = ServidorForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['data_nascimento'] = format_data_nascimento(cleaned_data['data_nascimento'])
            cleaned_data['cpf'] = format_cpf(cleaned_data['cpf'])
            cleaned_data['telefone'] = format_telefone(cleaned_data['telefone'])
            form.save()
            return redirect('cadastro_servidor')
    else:
        form = ServidorForm()

    # Obtenha todos os servidores
    servidores = Servidor.objects.all()

    # Ordenação
    if sort_field:
        servidores = servidores.order_by(sort_field)  # Aplica a ordenação com base no campo selecionado

    docentes = Docente.objects.all()
    cursos = Curso.objects.all()

    return render(request, 'cadastro_servidor.html', {'form': form, 'servidores': servidores, 'docentes': docentes, 'cursos': cursos})




def perfil_servidor(request, pk):
    servidor = Servidor.objects.get(pk=pk)
    documentos = Documento.objects.all
    return render(request, 'perfil_servidor.html', {'servidor' : servidor, 'documentos' : documentos})

def editar_servidor(request, pk):
    servidores = get_object_or_404(Servidor, pk=pk)
    if request.method == 'POST':
        form = ServidorForm(request.POST,instance=servidores)
        if form.is_valid():
            form.save()
            return redirect('cadastro_servidor')
    else:
        form = ServidorForm(instance=servidores)

    cursos = Curso.objects.all()  # Obtenha todos os cursos do banco de dados
    servidores = Servidor.objects.all()  # Obtenha todos os docentes do banco de dados

    return render(request, 'cadastro_servidor.html', {'form': form, 'cursos': cursos, 'servidores': servidores, })

from django.shortcuts import render, redirect
from .forms import DocumentoForm

def enviar_documento(request, pk):
    servidor = get_object_or_404(Servidor, pk=pk)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']

            # Verifica se já existe um documento com o mesmo tipo
            documento_existente = Documento.objects.filter(servidor=servidor, tipo=tipo).first()

            if documento_existente and not request.POST.get('substituir_documento'):
                return render(request, 'enviar_documento.html', {
                    'form': form,
                    'documento_existente': documento_existente,
                    'servidor': servidor
                })

            # Substitui o documento existente, se houver
            if documento_existente:
                documento_existente.arquivo.delete()
                documento_existente.delete()

            form.instance.servidor = servidor
            form.save()
            return redirect('documentos_enviados', pk=servidor.pk)
    else:
        form = DocumentoForm(initial={'servidor': servidor})

    return render(request, 'enviar_documento.html', {'form': form, 'servidor': servidor})



def documentos_enviados(request, pk):
    servidor = get_object_or_404(Servidor, pk=pk)
    documentos = Documento.objects.filter(servidor=servidor)
    return render(request, 'documentos_enviados.html', {'servidor': servidor, 'documentos': documentos})


def remover_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    servidor = documento.servidor
    documento.arquivo.delete()  # Remove o arquivo associado ao documento
    documento.delete()  # Remove o documento do banco de dados
    return redirect('documentos_enviados', pk=servidor.pk)

def substituir_documento(request, documento_id):
    documento_existente = get_object_or_404(Documento, id=documento_id)
    servidor = documento_existente.servidor

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento_existente)
        if form.is_valid():
            form.save()
            return redirect('documentos_enviados', pk=servidor.pk)
    else:
        form = DocumentoForm(instance=documento_existente, use_required_attribute=False)

    return render(request, 'substituir_documento.html', {'servidor': servidor, 'form': form})



from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Spacer
from django.shortcuts import render, get_object_or_404
from .models import Declaracao
from .forms import DeclaracaoForm  # Certifique-se de importar o formulário correto

from django.shortcuts import render, redirect
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
from .models import Declaracao
from .forms import DeclaracaoForm

def emitir_declaracao(request):
    sucesso = False  # Variável para indicar se a declaração foi emitida com sucesso

    if request.method == 'POST':
        form = DeclaracaoForm(request.POST)
        if form.is_valid():
            declaracao = form.save()

            # Criar um objeto BytesIO para armazenar o PDF em memória
            buffer = BytesIO()

            # Criar o objeto PDF, usando o objeto BytesIO como "arquivo"
            doc = SimpleDocTemplate(buffer, pagesize=letter)

            # Conteúdo do PDF (substitua com seus próprios dados)
            conteudo = []

            # Adicionar o cabeçalho da declaração
            style = ParagraphStyle(name='HeaderStyle', fontSize=12)
            cabecalho = [
                [Paragraph("Declaração", style), ""],
                [f"Nome do Docente: {declaracao.docente.nome}", f"Curso: {declaracao.curso.nome}"]
            ]
            conteudo.extend(cabecalho)

            # Adicionar uma linha de espaço
            conteudo.append([Spacer(1, 0.2*inch)])

            # Adicionar outros detalhes da declaração como objetos Flowable
            # Exemplo:
            # detalhes = [
            #     [Paragraph("Detalhes:", style), ""],
            #     [Paragraph("Descrição do detalhe 1", style), Paragraph("Descrição do detalhe 2", style)],
            # ]
            #
            # conteudo.extend(detalhes)

            # Construir a tabela de conteúdo
            tabela = Table(conteudo, colWidths=[200, 200], rowHeights=[50, 20])

            estilo = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            tabela.setStyle(estilo)

            # Adicionar a tabela ao conteúdo do PDF
            conteudo.append(tabela)

            # Construir o PDF
            doc.build(conteudo)

            # Retornar o PDF como resposta HTTP
            buffer.seek(0)
            response = FileResponse(buffer, as_attachment=True, filename='declaracao.pdf')
            sucesso = True
            return render(request, 'emitir_declaracao.html', {'form': form, 'sucesso': sucesso, 'declaracao': declaracao})

    else:
        form = DeclaracaoForm()

    return render(request, 'emitir_declaracao.html', {'form': form})
