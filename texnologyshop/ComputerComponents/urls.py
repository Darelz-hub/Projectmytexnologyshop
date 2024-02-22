from django.urls import path, re_path
import ComputerComponents.views as components

urlpatterns = [
    path('', components.MainPage.as_view()),
    path('test/', components.test),
    path('document/', components.DocumentationMain.as_view(), name='document'),
    path('document/documentation/', components.Documentation.as_view(), name='document_documentation'),
    path('products/<slug:type_product_components>', components.Products.as_view(), name='products'),
    path('baskets/', components.Baskets.as_view(), name='basket'),
    path('basket/delete/', components.BasketDelete.as_view(), name='basket_delete'),
]
