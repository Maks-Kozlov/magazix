from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from meta.models import ModelMeta
from mptt.models import MPTTModel, TreeForeignKey


class Category(ModelMeta, MPTTModel):
    """
    Модель категории товаров с поддержкой древовидной структуры (MPTT) и SEO-метаданных.
    Иерархия: Категория -> Подкатегория.
    """

    name = models.CharField(_("Название"), max_length=255)
    slug = models.SlugField(_("Слаг"), max_length=255, unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Родительская категория"),
    )
    image = models.ImageField(_("Изображение"), upload_to="catalog/categories/", blank=True)

    # SEO поля
    meta_title = models.CharField(_("Meta Title"), max_length=255, blank=True)
    meta_description = models.TextField(_("Meta Description"), blank=True)
    meta_keywords = models.CharField(_("Meta Keywords"), max_length=255, blank=True)

    _metadata = {
        "title": "meta_title",
        "description": "meta_description",
        "keywords": "get_meta_keywords",
        "image": "get_meta_image",
    }

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

    def get_meta_keywords(self):
        if self.meta_keywords:
            return [k.strip() for k in self.meta_keywords.split(",")]
        return []

    def get_meta_image(self):
        if self.image:
            return self.image.url
        return None

    def get_absolute_url(self):
        return reverse("catalog:category_detail", kwargs={"slug": self.slug})


class ProductType(ModelMeta, models.Model):
    """
    Модель типа товара или серии (например, ТМЛс, ТМЛ).
    Привязывается к конкретной категории.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="product_types",
        verbose_name=_("Категория"),
    )
    name = models.CharField(_("Название серии/типа"), max_length=255)
    slug = models.SlugField(_("Слаг"), max_length=255, unique=True)
    description = models.TextField(_("Описание"), blank=True)
    image = models.ImageField(_("Изображение"), upload_to="catalog/types/", blank=True)
    order = models.PositiveIntegerField(_("Порядок"), default=0)

    # SEO поля
    meta_title = models.CharField(_("Meta Title"), max_length=255, blank=True)
    meta_description = models.TextField(_("Meta Description"), blank=True)

    _metadata = {
        "title": "meta_title",
        "description": "meta_description",
        "image": "get_meta_image",
    }

    class Meta:
        verbose_name = _("Тип товара/Серия")
        verbose_name_plural = _("Типы товаров/Серии")
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    def get_meta_image(self):
        if self.image:
            return self.image.url
        return None

    def get_absolute_url(self):
        return reverse("catalog:type_detail", kwargs={"slug": self.slug})


class Product(ModelMeta, models.Model):
    """
    Модель конкретной позиции товара (SKU).
    """

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Тип товара/Серия"),
    )
    sku = models.CharField(_("Артикул"), max_length=100, unique=True)
    name = models.CharField(_("Название позиции"), max_length=255)
    multiplicity = models.PositiveIntegerField(_("Кратность"), default=1, help_text=_("Количество в упаковке"))
    unit = models.CharField(_("Ед. изм."), max_length=20, default=_("шт"))

    # SEO поля
    meta_title = models.CharField(_("Meta Title"), max_length=255, blank=True)
    meta_description = models.TextField(_("Meta Description"), blank=True)

    _metadata = {
        "title": "meta_title",
        "description": "meta_description",
        "image": "get_meta_image",
    }

    class Meta:
        verbose_name = _("Товар (SKU)")
        verbose_name_plural = _("Товары (SKU)")
        ordering = ["name"]

    def __str__(self):
        return f"{self.sku} - {self.name}"

    def get_meta_image(self):
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image.image.url
        return None

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"sku": self.sku})


class ProductImage(models.Model):
    """
    Дополнительные изображения для товара.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Товар"),
    )
    image = models.ImageField(_("Изображение"), upload_to="catalog/products/gallery/")
    alt_text = models.CharField(_("Alt текст"), max_length=255, blank=True)
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    is_main = models.BooleanField(_("Главное изображение"), default=False)

    class Meta:
        verbose_name = _("Изображение товара")
        verbose_name_plural = _("Изображения товаров")
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.product.sku}"
