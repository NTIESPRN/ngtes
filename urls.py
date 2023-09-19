from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from .views import register_view
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('cadastro/docente/', views.cadastro_docente, name='cadastro_docente'),
    path('cadastro/docente/editar/<int:pk>/', views.editar_docente, name='editar_docente'),
    path('cadastro/curso/', views.cadastro_curso, name='cadastro_curso'),
    path('cadastro/curso/editar/<int:pk>/', views.editar_curso, name='editar_curso'),
    path('cadastro/servidor/', views.cadastro_servidor, name='cadastro_servidor'),
    path('cadastro/servidor/editar/<int:pk>/', views.editar_servidor, name='editar_servidor'),
    path('cadastro/servidor/perfil/<int:pk>/', views.perfil_servidor, name='perfil_servidor'),
    path('cadastro/servidor/enviar-documento/<int:pk>/', views.enviar_documento, name='enviar_documento'),
    path('cadastro/servidor/documentos-enviados/<int:pk>/', views.documentos_enviados, name='documentos_enviados'),
    path('remover-documento/<int:documento_id>/', views.remover_documento, name='remover_documento'),
    path('substituir-documento/<int:documento_id>/', views.substituir_documento, name='substituir_documento'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('export_excel/', views.export_to_excel, name='export_to_excel'),
    path('perfil_docente/<int:docente_id>/', views.perfil_docente, name='perfil_docente'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/profile/', auth_views.LoginView.as_view(template_name='perfil.html'), name='profile'),
    path('declaracao/', views.emitir_declaracao, name='emitir_declaracao'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

