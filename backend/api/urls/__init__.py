from django.urls import path, include
from api.urls import user as user_urls
from api.urls import farm as farm_urls
from api.urls import fieldboundary as fieldboundary_urls

urlpatterns = [
    path("users/", include((user_urls.urlpatterns))),
    path("", include((fieldboundary_urls.urlpatterns))),
    path("", include((farm_urls.urlpatterns))),
]
