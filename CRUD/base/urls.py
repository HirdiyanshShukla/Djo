from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="base_home"),
    path('room/<str:pk>/', views.room, name="base_room"),
    path('createroom/', views.create_room, name="create_room"),
    path('updateroom/<str:pk>/', views.update_room, name="update_room"),
    path('deleteroom/<str:pk>/', views.delete_room, name="delete_room"),
    path('login/', views.LoginPage, name="login"),
    path('logout/', views.LogoutUser, name="logout"),
    path('register/', views.Registerpage, name="register"),
    path('deletemessage/<str:pk>/', views.delete_message, name="delete_message"),
    path('userprofile/<str:pk>/', views.userprofile, name='userprofile')

]