from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin

from .models import Category
from .models import Product
from .models import ProductImage
from .models import ProductType


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image", "alt_text", "order", "is_main"]


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = (
        "tree_actions",
        "indented_title",
        "slug",
    )
    list_display_links = ("indented_title",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")

    fieldsets = (
        (None, {"fields": ("name", "slug", "parent", "image")}),
        (_("SEO"), {"fields": ("meta_title", "meta_description", "meta_keywords")}),
    )


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug", "description")
    ordering = ("category", "order", "name")

    fieldsets = (
        (None, {"fields": ("category", "name", "slug", "description", "image", "order")}),
        (_("SEO"), {"fields": ("meta_title", "meta_description")}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "product_type", "multiplicity", "unit")
    list_filter = ("product_type__category", "product_type")
    search_fields = ("sku", "name")
    inlines = [ProductImageInline]

    fieldsets = (
        (None, {"fields": ("product_type", "sku", "name", "multiplicity", "unit")}),
        (_("SEO"), {"fields": ("meta_title", "meta_description")}),
    )
