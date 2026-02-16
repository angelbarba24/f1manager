from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Login / Logout
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Rutas de la App
    path('', views.home, name='home'),
    path('parrilla/', views.parrilla_2026, name='parrilla'),
    path('calendario/', views.calendario_2026, name='calendario'),
    path('predicciones/', views.lista_predicciones, name='lista_predicciones'),
    path('prediccion/nueva/', views.crear_prediccion, name='crear_prediccion'),
    path('prediccion/editar/<int:pk>/', views.editar_prediccion, name='editar_prediccion'),
    path('prediccion/borrar/<int:pk>/', views.borrar_prediccion, name='borrar_prediccion'),
    path('favorito/toggle/<int:piloto_id>/', views.toggle_favorito, name='toggle_favorito'),
    path('mis-favoritos/', views.mis_favoritos, name='mis_favoritos'),
]