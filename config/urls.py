from django.urls import (
    include,
    path,
)

urlpatterns = [
    path("", include("apps.core.urls")),
    path("api/accounts/v1/", include("rest_registration.api.urls")),
    path("api/admin/v1/", include("apps.users.api.v1.urls")),
    path('api/watch_list/v1/', include("apps.stock_watcher.api.v1.urls")),
]
