from django.urls import path
from .views import PageView, EditPage, CreatePage

app_name = 'cms'

urlpatterns = [
    path('edit/', EditPage.as_view(), name='editpage'),
    path('<slug:slug>/edit/', EditPage.as_view(), name='editpage'),
    path('createpage/', CreatePage.as_view(), name='createpage'),
    path('', PageView.as_view(), name='page'),
    path('<slug:slug>/', PageView.as_view(), name='page'),
]
