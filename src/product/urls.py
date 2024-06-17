from product import views
from django.urls import path


urlpatterns = [
    path(
        route="health/",
        view=views.HealthCheck.as_view(),
        name="health",
    ),
    path(
        route="products/",
        view=views.Products.as_view(),
        name="health",
    ),
    path(
        route="products/<int:product_id>",
        view=views.Products.as_view(),
        name="health",
    ),
]
