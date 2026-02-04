from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import DetailView
from django.views.generic import ListView
from meta.views import MetadataMixin

from .models import Category
from .models import Product
from .models import ProductType


def category_products_partial(request, slug):
    """Partial view для загрузки списка товаров категории через AJAX."""
    category = get_object_or_404(Category, slug=slug, parent=None)
    
    # Получить все подкатегории (потомки)
    subcategory_ids = category.get_descendants().values_list("id", flat=True)
    
    # Товары из всех подкатегорий
    products = Product.objects.filter(
        product_type__category_id__in=subcategory_ids
    ).select_related("product_type", "product_type__category").prefetch_related("images")
    
    # Пагинация
    per_page_options = [24, 36, 48, 72]
    try:
        per_page = int(request.GET.get("per_page", 24))
        if per_page not in per_page_options:
            per_page = 24
    except (ValueError, TypeError):
        per_page = 24
    
    paginator = Paginator(products, per_page)
    page = request.GET.get("page", 1)
    products_page = paginator.get_page(page)
    
    context = {
        "category": category,
        "products": products_page,
        "products_count": paginator.count,
        "view_mode": request.GET.get("view", "list"),
        "per_page": per_page,
        "per_page_options": per_page_options,
    }
    
    return TemplateResponse(request, "catalog/_products_list.html", context)


class CategoryListView(ListView):
    model = Category
    template_name = "catalog/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(parent=None).prefetch_related("children")


class CategoryDetailView(MetadataMixin, DetailView):
    model = Category
    template_name = "catalog/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        return Category.objects.select_related("parent").prefetch_related("children", "product_types")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = self.object.as_meta(self.request)
        
        category = self.object
        
        # Только для категорий верхнего уровня (без родителя) показываем товары
        if category.parent is None:
            # Получить все подкатегории (потомки)
            subcategory_ids = category.get_descendants().values_list("id", flat=True)
            
            # Товары из всех подкатегорий
            products = Product.objects.filter(
                product_type__category_id__in=subcategory_ids
            ).select_related("product_type", "product_type__category").prefetch_related("images")
            
            # Пагинация
            per_page_options = [24, 36, 48, 72]
            try:
                per_page = int(self.request.GET.get("per_page", 24))
                if per_page not in per_page_options:
                    per_page = 24
            except (ValueError, TypeError):
                per_page = 24
            
            paginator = Paginator(products, per_page)
            page = self.request.GET.get("page", 1)
            products_page = paginator.get_page(page)
            
            context["products"] = products_page
            context["products_count"] = paginator.count
            context["view_mode"] = self.request.GET.get("view", "list")
            context["per_page"] = per_page
            context["per_page_options"] = per_page_options
        
        return context


class ProductTypeDetailView(MetadataMixin, DetailView):
    model = ProductType
    template_name = "catalog/type_detail.html"
    context_object_name = "product_type"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = self.object.as_meta(self.request)
        return context


class ProductDetailView(MetadataMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        return Product.objects.get(sku=self.kwargs.get("sku"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = self.object.as_meta(self.request)
        return context
