
from django.urls import path
from gamestoreapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('create_product', views.createproduct),
    path('read_products', views.read_products),
    path('register', views.register_user),
    path('update_products/<rid>', views.update_products),
    path('delete/<rid>',  views.delete),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('create_cart/<rid>', views.create_cart),
    path('read_cart', views.read_cart),
    path('delete_cart/<rid>', views.delete_cart),
    path('update_cart/<cid>/<q>', views.update_cart),
    path('create_orders/<rid>', views.create_orders),
    path('read_orders', views.read_orders),
    path('create_review/<rid>', views.create_review),
    path('readproductdetails/<rid>', views.productdetail),
    path('forgot_password', views.forgotPassword),
    path('opt_verification', views.opt_verification),
    path('reset_password', views.reset_password)
]

urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)