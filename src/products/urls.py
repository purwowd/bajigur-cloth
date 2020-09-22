from django.urls import path

from . import views

urlpatterns = [
    # path('', views.product_list, name='product-list'),
    path('product-detail/<product_id>/', views.product_detail, name='product-detail'),
    path('review-detail/<review_id>/', views.review_detail, name='review-detail'),
    path('review-list/', views.review_list, name='review-list'),
    path('user-review/', views.user_review_list, name='user-review-list'),
    path('recommend/', views.user_recommendation_list, name='user-recommend-list'),
    path('product-detail/<product_id>/add-review/', views.add_review, name='add-review'),
]
