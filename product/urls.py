from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path("", home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.ContactView, name='contact'),
    path('shop/<int:pk>', views.ShopView, name='shop'),
    path('cart/', views.CartView, name='cart'),
    path('add_item/<int:pk>/', views.CartItemAddView, name='cart_add'),
    path('remove_item/<int:pk>/', views.CartItemRemoveView, name='cart_remove'),
    path('categories/<str:slug>/', views.CategoriesView, name='categories'),
    path('item/delete/<int:pk>/', views.DeleteItemCart, name='item_delete'),
    path('product/filter/<int:minimum>/<int:maximum>/', views.ProductFilterView, name='product_filter'),
    path('search/', views.SearchView, name='search'),
    path('product/<int:pk>/', views.DetailPageView, name='detailpage'),
    path('detailpageadditem/<int:pk>/', views.DetailAddCart, name="detail_add_cart"),
    path("comment-add/<int:pk>/", views.CommentAddView, name="add_comment")

]