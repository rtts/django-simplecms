from django.urls import path
from .views import PageView, CreatePage, UpdatePage, CreateSection, UpdateSection

app_name = 'cms'

urlpatterns = [
    path('new/', CreatePage.as_view(), name='createpage'),
    path('edit/', UpdatePage.as_view(), kwargs={'slug': ''}, name='updatepage'),
    path('edit/<int:number>/', UpdateSection.as_view(), kwargs={'slug': ''}, name='updatesection'),
    path('<slug:slug>/edit/', UpdatePage.as_view(), name='updatepage'),
    path('<slug:slug>/edit/new/', CreateSection.as_view(), name='createsection'),
    path('<slug:slug>/edit/<int:number>/', UpdateSection.as_view(), name='updatesection'),
    path('', PageView.as_view(), name='page'),
    path('<slug:slug>/', PageView.as_view(), name='page'),
]
