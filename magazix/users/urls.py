from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view
from .views import user_card_view
from .views import user_card_edit_view
from .views import user_card_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("demo/card/", view=user_card_view, name="card"),
    path("demo/card/edit/", view=user_card_edit_view, name="card_edit"),
    path("demo/card/update/", view=user_card_update_view, name="card_update"),
]
