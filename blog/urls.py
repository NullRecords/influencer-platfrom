from django.urls import path
from wagtail.contrib.sitemaps.views import sitemap
from wagtail import urls as wagtail_urls

urlpatterns = [
    path("sitemap.xml", sitemap),
    path("", include(wagtail_urls)),
]
