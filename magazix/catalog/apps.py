from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "magazix.catalog"
    verbose_name = _("Каталог")

    def ready(self):
        try:
            import magazix.catalog.signals  # noqa: F401
        except ImportError:
            pass
