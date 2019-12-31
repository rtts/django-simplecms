from django.urls import path
from .views import PageView, UpdatePage, CreatePage, UpdateSection, CreateSection

app_name = 'cms'

urlpatterns = [
    path('updatepage/', UpdatePage.as_view(), {'slug': ''}, name='updatehomepage'),
    path('updatepage/<int:pk>/', UpdatePage.as_view(), name='updatepage'),
    path('updatesection/<int:pk>/', UpdateSection.as_view(), name='updatesection'),
    path('createpage/', CreatePage.as_view(), name='createpage'),
    path('createsection/<int:pk>', CreateSection.as_view(), name='createsection'),

    # Feel free to copy the following into your root URL conf!
    path('', PageView.as_view(), name='page'),
    path('<slug:slug>/', PageView.as_view(), name='page'),
]
