# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('product/<slug:slug>/', views.product_detail, name='product_detail'),
#     path('add/', views.add_product, name='add_product'),
#     path('cart/', views.cart_view, name='cart'),
#     path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
]
