from __future__ import absolute_import
from django.contrib import admin
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .api import DocumentTableViewSet, DocumentFieldViewSet, DocumentFieldCreateView, DocumentTableCreateView

admin.autodiscover()

router = DefaultRouter()
router.register(r'table', DocumentTableViewSet)
router.register(r'fields', DocumentFieldViewSet)

urlpatterns = (
    url(r'admin/', include(admin.site.urls)),
    url(r'documentfield-create/', DocumentFieldCreateView.as_view(),
        name='documentfield-create'),
    url(r'documenttable-create/', DocumentTableCreateView.as_view(),
        name='documenttable-create'),


    url(r'api/', include(router.urls, namespace='api')),
)
