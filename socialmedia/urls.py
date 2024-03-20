from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm


app_name = 'social'
urlpatterns = [
    path('', views.index, name='index'),
    # path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login', ),
    path('logout/', views.log_out, name='logout', ),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    # path('user/edit/', views.edit_account, name='edit_account')

]
