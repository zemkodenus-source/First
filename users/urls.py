from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Стандартна Django авторизація
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.register , name = 'registration'),
    path('profile/',views.profile , name = 'profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),                   # Стандартна Django авторизація
    path('login_exit' , auth_views.LogoutView.as_view(template_name='users/login_exit.html'), name='login_exit'),    # Стандартна Django для виходу (де_авторизація)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)