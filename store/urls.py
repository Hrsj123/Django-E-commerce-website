from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),         # backend page! (it recieves the data from client and processes it in views.py)
    path('process_order/', views.processOrder, name="process_order"),         # backend page! (it recieves the data from client and processes it in views.py)
]