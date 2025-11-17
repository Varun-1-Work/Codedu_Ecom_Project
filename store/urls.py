from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('collections/', views.collections, name='collections'),
    path('login/', views.loginn, name='login'),
    path('register/', views.register, name='register'),
    path('blog/', views.blog_list, name='blog'),
    path('about/', views.about, name='about'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('product/', views.product, name='product'),
    path('contact/', views.contact, name='contact'),

    # Cart URLs
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Debug View
    path('debug-cart/', views.debug_cart, name='debug_cart'),

    path('logout/', views.logout, name='logout'),

]
