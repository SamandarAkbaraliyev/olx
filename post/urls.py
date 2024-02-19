from django.urls import path
from post import views

urlpatterns = [
    path('category-list/', views.CategoryParentListAPIView.as_view()),
    path('category-list/<slug:parent>/', views.CategoryListAPIView.as_view()),


    path('', views.MainPostListAPIView.as_view()),
    path('<slug:slug>/', views.PostDetailAPIView.as_view()),
]

