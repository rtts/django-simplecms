from django.urls import path
from .views import PageView, UpdatePage, CreatePage, CreateSection

app_name = 'cms'

urlpatterns = [
    path('', PageView.as_view(), {'slug': ''}, name='homepage'),
    path('<slug:slug>/', PageView.as_view(), name='page'),
    path('cms/homepage/', UpdatePage.as_view(), {'slug': ''}, name='updatehomepage'),
    path('cms/page/<slug:slug>/', UpdatePage.as_view(), name='updatepage'),
    path('cms/newpage/', CreatePage.as_view(), name='createpage'),
    #path('cms/page/<slug:slug>/createsection/', CreateSection.as_view(), name='createsection'),
]
