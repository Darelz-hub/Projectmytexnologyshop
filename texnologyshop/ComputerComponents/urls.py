from django.urls import path, re_path
import ComputerComponents.views as components

urlpatterns = [
    # path('videocard/', components.videocard),
    # re_path(r"^videocardyear/(?P<year>[0-9]{4})/$", components.videocardyear),
    path('test/', components.test),
    # path('<slug:name_page>', components.components_pages),
    path('document/', components.documentationmain),
    path('document/documentation/', components.documentation),
]
