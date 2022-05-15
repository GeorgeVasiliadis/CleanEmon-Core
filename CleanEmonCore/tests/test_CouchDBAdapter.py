from pytest import fixture

from CleanEmonCore import CONFIG_FILE
from CleanEmonCore.CouchDBAdapter import CouchDBAdapter
from CleanEmonCore.models import EnergyData

TEST_DB_NAME = "test_db"
DUMMY_DATE = "2000-01-01"


@fixture
def energy_data():
    return EnergyData(DUMMY_DATE,
                      [
                          {"timestamp": 1,
                           "power": 100,
                           "temp": 20
                           },
                          {"timestamp": 2,
                           "power": 150,
                           "temp": 21
                           },
                          {"timestamp": 3,
                           "power": 120,
                           "temp": 21
                           }
                      ])


@fixture
def adapter():
    return CouchDBAdapter(CONFIG_FILE)


@fixture
def document(adapter):
    yield adapter.create_document(TEST_DB_NAME)
    adapter.delete_document(TEST_DB_NAME)


@fixture
def populated_document(adapter, energy_data):
    yield adapter.create_document(TEST_DB_NAME, initial_data=energy_data)
    adapter.delete_document(TEST_DB_NAME)


class TestCreateDelete:
    def test_create_delete_document(self, adapter):
        assert adapter.create_document(TEST_DB_NAME)
        assert adapter.delete_document(TEST_DB_NAME)

    def test_double_create_delete_document(self, adapter):
        assert adapter.create_document(TEST_DB_NAME)
        assert not adapter.create_document(TEST_DB_NAME)
        assert adapter.delete_document(TEST_DB_NAME)
        assert not adapter.delete_document(TEST_DB_NAME)

    def test_create_initialized_document(self, adapter, energy_data):
        assert adapter.create_document(TEST_DB_NAME, initial_data=energy_data)
        assert adapter.delete_document(TEST_DB_NAME)


class TestFetchUpdate:
    def test_fetch_document(self, adapter, document):
        doc = adapter._fetch_document(document=document)
        assert doc
        assert "_id" in doc
        assert "_rev" in doc

    def test_update_document(self, adapter, document):
        assert adapter._update_document({"test": "helloworld"}, document=document)
        doc = adapter._fetch_document(document=document)
        assert doc
        assert "_id" in doc
        assert "_rev" in doc
        assert "test" in doc


class TestEnergyData:
    def test_fetch_energy_data(self, adapter, document):
        energy_data = adapter.fetch_energy_data(document=document)
        assert type(energy_data) is EnergyData

    def test_append_energy_data(self, adapter, document, energy_data):
        assert adapter.append_energy_data(energy_data, document=document)
        data = adapter.fetch_energy_data(document=document)
        assert data
        assert len(data.energy_data) > 0


class TestByDate:
    def test_get_document_id_for_date(self, adapter, populated_document):
        assert populated_document == adapter.get_document_id_for_date(DUMMY_DATE)

    def test_fetch_energy_data_by_date(self, adapter, populated_document):
        data = adapter.fetch_energy_data_by_date(DUMMY_DATE)
        assert data
        assert DUMMY_DATE == data.date

    def test_update_energy_data_by_date(self, adapter, energy_data, populated_document):
        assert adapter.update_energy_data_by_date(DUMMY_DATE, energy_data)
        data = adapter.fetch_energy_data_by_date(DUMMY_DATE)
        assert data == energy_data
