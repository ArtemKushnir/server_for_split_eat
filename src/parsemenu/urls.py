from django.contrib import admin
from django.urls import path
from .views import TaskView, ParseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-task/', TaskView),
    path('parse/', ParseView)
]
