from django.urls import path

from .views import CategoryListView, RestaurantsListView

urlpatterns = [
    path("list-restaurants", RestaurantsListView.as_view()),
    path("list-categories", CategoryListView.as_view()),
]
