from django.urls import path

from .views import ActiveUserOrdersView, CartView

urlpatterns = [path("", CartView.as_view()), path("orders-user-active/", ActiveUserOrdersView.as_view())]
