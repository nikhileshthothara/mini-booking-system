from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('quickbook.urls', namespace='quickbook')),
    path('auth/', include('authbase.urls', namespace='authbase')),
]

urlpatterns += [
    path('admin/', admin.site.urls),
]
