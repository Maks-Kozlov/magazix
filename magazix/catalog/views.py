from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.generic import ListView
from meta.views import MetaDetailViewMixin

from .models import Category
from .models import Product
from .models import ProductType


class CategoryListView(ListView):
    model = Category
    template_name = "catalog/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(MetaDetailViewMixin, DetailView):
    model = Category
    template_name = "catalog/category_detail.html"
    context_object_name = "category"


class ProductTypeDetailView(MetaDetailViewMixin, DetailView):
    model = ProductType
    template_name = "catalog/type_detail.html"
    context_object_name = "product_type"


class ProductDetailView(MetaDetailViewMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        return Product.objects.get(sku=self.kwargs.get("sku"))
