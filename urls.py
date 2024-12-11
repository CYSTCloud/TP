from django.contrib import admin
from django.urls import path
from translator.views import TranslationAPI, index

try:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    SCHEMA_VIEW_ENABLED = True
except ImportError:
    SCHEMA_VIEW_ENABLED = False

# API Schema configuration (if drf_yasg is available)
if SCHEMA_VIEW_ENABLED:
    schema_view = get_schema_view(
        openapi.Info(
            title="Polyteacher Translation API",
            default_version="v1",
            description="API for translating text between supported languages.",
            terms_of_service="https://www.adou.org/terms/",
            contact=openapi.Contact(email="support@adou.org"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
    )

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('', index, name='home'),  # Index view
    path('api/translation/', TranslationAPI.as_view(), name='translation_endpoint'),  # Translation endpoint
]

if SCHEMA_VIEW_ENABLED:
    urlpatterns += [
        path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='api_docs'),  # API documentation
    ]
