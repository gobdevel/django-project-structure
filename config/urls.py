from django.urls import (
    include,
    path,
)

urlpatterns = [
    path("", include("apps.core.urls")),
    path("api/accounts/v1/", include("rest_registration.api.urls")),
    path("api/admin/v1/", include("apps.users.api.v1.urls")),
]
