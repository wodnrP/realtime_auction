from django.urls import path
from product import views

urlpatterns = [
    path("all-products", views.ProductsView.as_view(), name="all-products"),
]
