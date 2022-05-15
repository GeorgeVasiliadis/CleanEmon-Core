from pytest import fixture

from CleanEmonCore.models import EnergyData


@fixture
def energy_data():
    return EnergyData("2022-05-01",
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


class TestEnergyData:

    def test_init(self, energy_data):
        data = energy_data
        assert data.date

    def test_as_json(self, energy_data):
        data = energy_data
        assert data.energy_data
        assert type(data.as_json(string=True)) is str
        assert type(data.as_json(string=False)) is dict