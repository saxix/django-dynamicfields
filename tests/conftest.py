import pytest
from django_dynamic_fixture import G

from demoproject.models import DocumentTable, DocumentField


@pytest.fixture(scope='session')
def client(request):
    import django_webtest
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    app = django_webtest.DjangoTestApp()
    return app


@pytest.fixture()
def document_table():
    return G(DocumentTable)


@pytest.fixture()
def document_field():
    return G(DocumentField,
             fields=None)
