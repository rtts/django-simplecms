from django.urls import path
from .views import PageView, CreatePage, UpdatePage

app_name = 'cms'

urlpatterns = [
    path('new/', CreatePage.as_view(), name='createpage'),
    path('edit/', UpdatePage.as_view(), name='updatepage'),
    path('<slug:slug>/edit/', UpdatePage.as_view(), name='updatepage'),
    path('', PageView.as_view(), name='page'),
    path('<slug:slug>/', PageView.as_view(), name='page'),
]
