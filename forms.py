from django import forms
from .models import Docente, Curso, DeclaracaoEmitida

class DocenteForm(forms.ModelForm):
    form_name = 'DocenteForm'
    class Meta:
        model = Docente
        exclude = ['cursos']
    telefone = forms.CharField(widget=forms.TextInput(attrs={'data-mask': '(00) 00000-0000'}))


        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'id':  # Excluir o campo 'id' se você não quiser incluí-lo no formulário
                self.fields[field].widget.attrs['class'] = 'validate'

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'id':  # Excluir o campo 'id' se você não quiser incluí-lo no formulário
                self.fields[field].widget.attrs['class'] = 'validate'

from .models import Servidor


class ServidorForm(forms.ModelForm):
    form_name = 'ServidorForm'
    class Meta:
        model = Servidor
        exclude = ['cursos']
    telefone = forms.CharField(widget=forms.TextInput(attrs={'data-mask': '(00) 00000-0000'}))


        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'id':  # Excluir o campo 'id' se você não quiser incluí-lo no formulário
                self.fields[field].widget.attrs['class'] = 'validate'

from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'id':  # Excluir o campo 'id' se você não quiser incluí-lo no formulário
                self.fields[field].widget.attrs['class'] = 'validate'

class DeclaracaoEmitidaForm(forms.ModelForm):
    class Meta:
        model = DeclaracaoEmitida
        fields = ['docente', 'curso', 'componente']