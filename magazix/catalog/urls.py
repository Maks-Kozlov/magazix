from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.CategoryListView.as_view(), name="category_list"),
    path("category/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("type/<slug:slug>/", views.ProductTypeDetailView.as_view(), name="type_detail"),
    path("product/<str:sku>/", views.ProductDetailView.as_view(), name="product_detail"),
]
