from django.urls import path
from . import views

app_name = 'Maria_membership'

urlpatterns = [
    path('', views.home, name='home'),
    path('information/', views.information, name='information'),
    path('reqfacePicture/', views.reqfacePicture, name='reqfacePicture'),
    path('reqfaceRecog/', views.reqfaceRecog, name='reqfaceRecog'),
    path('menu/', views.menu, name='menu'),
    path('stamp/', views.stamp, name='stamp'),
    path('mypage/',views.mypage, name='mypage'),
    path('order_complete',views.order_complete,name='order_complete'),
]