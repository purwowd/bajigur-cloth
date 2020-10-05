from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('update-item/', views.update_item, name='update-item'),
    path('checkout/', views.checkout, name="checkout"),
    path('process-order/', views.process_order, name='process-order'),
]
