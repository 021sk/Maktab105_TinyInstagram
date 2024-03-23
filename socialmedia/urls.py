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
    path('user/edit/', views.edit_user, name='edit_account'),

    path('ticket/', views.ticket, name="ticket"),

    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete'),
         name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]
