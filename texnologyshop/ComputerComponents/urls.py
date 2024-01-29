from django.urls import path, re_path
import ComputerComponents.views as components

urlpatterns = [
    path('', components.MainPage.as_view()),
    #path('', components.main),
    # path('videocard/', components.videocard),
    # re_path(r"^videocardyear/(?P<year>[0-9]{4})/$", components.videocardyear),
    path('test/', components.test),
    # path('<slug:name_page>', components.components_pages),
    path('document/', components.DocumentationMain.as_view()),
    path('document/documentation/', components.Documentation.as_view()),
    path('products/<slug:type_product_components>', components.Products.as_view()),
    # path('document/', components.documentationmain),
    # path('document/documentation/', components.documentation),
]
