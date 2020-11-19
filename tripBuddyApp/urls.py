from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('travels', views.success),
    path('logout', views.logout),
    path('addtrip', views.tripForm),
    path('createTrip', views.createTrip),
    path('view/<int:tripID>', views.viewTrip),
    path('join/<int:tripID>', views.joinTrip),
    path('cancel/<int:tripID>', views.cancelTrip),
    path('delete/<int:tripID>', views.deleteTrip),
]