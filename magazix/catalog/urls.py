from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.CategoryListView.as_view(), name="category_list"),
    path("category/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("category/<slug:slug>/products/", views.category_products_partial, name="category_products_partial"),
    path("type/<slug:slug>/", views.ProductTypeDetailView.as_view(), name="type_detail"),
    path("product/<str:sku>/", views.ProductDetailView.as_view(), name="product_detail"),
]
