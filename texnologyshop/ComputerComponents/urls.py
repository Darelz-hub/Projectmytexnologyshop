from django.urls import path
import ComputerComponents.views as components


urlpatterns = [
    path('videocard/<int:id_cc>/', components.videocard)
]
