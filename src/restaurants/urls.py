from django.urls import path

from .views import MenuCategoryListView, RestaurantCategoryListView, RestaurantMenuListView, RestaurantsListView

urlpatterns = [
    path("list-restaurants", RestaurantsListView.as_view()),
    path("list-categories", RestaurantCategoryListView.as_view()),
    path("list-menu-categories", MenuCategoryListView.as_view()),
    path("list-restaurant-menu", RestaurantMenuListView.as_view()),
]
