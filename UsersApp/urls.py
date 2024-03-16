from django.urls import path
from .views import *

urlpatterns = [
        path('login/',loginUser,name="login-page"),
    path('logout/',logoutUser,name="logout-page"),
        path('signup/',signUpUser,name="signup-page"),
        path('forgot_password/',forgot_password,name="forgot_password"),
    path('',index,name='index'),
    path('categories/',categories,name='categories'),
    path('products/<int:category>',products,name='products'),
    path('add_to_cart/<int:product_id>/',add_to_cart,name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('remove_from_cart/<int:product_id>/<str:action>',remove_from_cart,name='remove_from_cart'),
    path('add_to_wishlist/<int:product_id>/',add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/',wishlist,name='wishlist'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('feedback/',feedback,name='feedback'),
    path('list_feedback/',list_feedback,name='list_feedback'),
    path('inventory/',inventory,name='inventory'),
    path('update_inventory/<int:prod_id>/<str:action>/',update_inventory,name='update_inventory'),
    path('staff_login/',staff_login,name='staff_login'),
]