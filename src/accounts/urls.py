from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('auth/', views.auth, name='auth'),
    path('logout/', views.sign_out, name='sign_out'),
]
