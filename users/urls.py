from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path('login/', views.LoginView, name='login'),
    path('signup/', views.SignUpView, name='signup'),
    path('confirm-code/<str:uniq_id>/', views.ConfirmEmailView, name='confirm_code'),
    path('profile/<str:uniq_id>/', views.ProfileView, name='profile'),
    path('logout/<str:uniq_id>/', views.LogoutView, name="logout")
]