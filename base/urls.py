from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('create-post/', views.create_post, name='create_post'),
    path('update-post/<str:pk>', views.update_post, name='update_post'),
    path('signup/', views.signup, name='signup'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
]