from django.urls import path
import ComputerComponents.views as components

urlpatterns = [
    path('', components.MainPage.as_view(), name='main_page'),
    #path('test/', components.test),
    path('document/', components.DocumentationMain.as_view(), name='document'),
    path('document/documentation/', components.Documentation.as_view(), name='document_documentation'),
    path('products/<slug:category>', components.Products.as_view(), name='products'),
    path('products/<slug:category>/<slug:subcategory>', components.ProductsSubcategory.as_view(), name='products'),
    path('baskets/', components.Baskets.as_view(), name='basket'),
    path('baskets/add_product/', components.BasketAddProduct.as_view(), name='basket_add_product'),
    path('basket/delete/', components.BasketDeleteProduct.as_view(), name='basket_delete_product'),
    path('order/', components.FormOrder.as_view(), name='form_order'),
    path('create_order/', components.CreateOrder.as_view(), name='create_order'),
    path('ceal_order/', components.CealOrder.as_view(), name='ceal_order'),
    path('payment_success/', components.PaymentSuccess.as_view(), name='payment_success'),
    #path('payment_failed/', components.PaymentFailed.as_view(), name='payment_failed'),
    path('delivery/', components.PageDelivery.as_view(), name='delivery'),
    path('page_order/', components.PageOrder.as_view(), name='page_order'),
    path('order_products_delete/', components.OrderProductsDelete.as_view(), name='order_products_delete'),
    path('search_products/', components.SearchProducts.as_view(), name='search')
]
