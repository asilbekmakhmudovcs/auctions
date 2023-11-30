from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new/", views.new_product, name="new_product"),
    path("auction/<str:pk>", views.product, name='product'),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("delete/<str:pk>", views.delete_product, name="delete_product"),
    path('sell/<str:pk>', views.sell_product, name='sell_product'),
    path("own/", views.owned_products, name="owned_products"),
    path("re_auction/<str:pk>", views.re_auction, name='re_auction'),
]
