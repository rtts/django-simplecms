from django.urls import path
from .views import PageView, UpdatePage, CreatePage, UpdateSection, CreateSection, CreateSubSection

app_name = 'cms'

urlpatterns = [
    path('', PageView.as_view(), {'slug': ''}, name='homepage'),
    path('<slug:slug>/', PageView.as_view(), name='page'),
    path('cms/homepage/', UpdatePage.as_view(), {'slug': ''}, name='updatehomepage'),
    path('cms/page/<int:pk>/', UpdatePage.as_view(), name='updatepage'),
    path('cms/section/<int:pk>/', UpdateSection.as_view(), name='updatesection'),
    path('cms/newpage/', CreatePage.as_view(), name='createpage'),
    path('cms/page/<int:pk>/newsection/', CreateSection.as_view(), name='createsection'),
    path('cms/section/<int:pk>/newsubsection/', CreateSubSection.as_view(), name='createsubsection'),
]
