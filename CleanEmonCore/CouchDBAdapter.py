"""Database-related communication module"""

import configparser
import json
from typing import Dict

import requests

from .models import EnergyData
from . import json_utils


class CouchDBAdapter:
    """CouchDB Adapter class used to exchange data using REST API."""

    def __init__(self, config_file: str):

        # Load configuration file
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(config_file)

        self.endpoint = cfg["DB"]["endpoint"]
        self.db = "emon_" + self.get_emon_pi_serial()
        self.username = cfg["DB"]["username"]
        self.password = cfg["DB"]["password"]
        self.base_url = f"{self.endpoint}"

    @staticmethod
    def get_emon_pi_serial() -> str:
        """
        :return: the device ID of the EmonPi.
        """
        from os.path import exists
        serial = "no-serial"
        if exists("/sys/firmware/devicetree/base/serial-number"):
            with open("/sys/firmware/devicetree/base/serial-number", 'r') as f:
                serial = f.read().rstrip('\x00').lstrip('0').lower()
        return serial

    def _fetch_document(self, *, document: str, db: str = None) -> dict:
        """Fetches the default document.
        Returns its content in json-format. If operation is unsuccessful, an
        empty dict is being returned.

        document -- The document to be fetched. It is usually omitted as the
                    default document is being implied, but an arbitrary document
                    can be specified as well.

        Throws:
        AssertionError -- If no document can be found.
        """

        if not db:
            db = self.db

        assert document, "No document was supplied!"
        assert db, "No database name was supplied!"

        res = requests.get(f"{self.base_url}/{db}/{document}",
                           auth=(self.username, self.password))

        data = {}

        if res.ok:
            data = res.json()

        return data

    def _update_document(self, data: dict, *, document, db: str = None) -> bool:
        """Updates the default document with the given data. This is equivalent
        to overwriting the stored data. Use with caution!
        Returns True if the document was updated successfully.

        data -- The data that will be used to update the specified document. If omitted, an empty dictionary
        will be passed instead, which will be equivalent to dropping the previous document.
        document -- The document to be updated. It is usually omitted as the
                    default document is being implied, but an arbitrary document
                    can be specified as well.

        Throws:
        AssertionError -- If no document can be found.
        """

        if not db:
            db = self.db

        assert document, "No document was supplied!"
        assert db, "No database name was supplied!"

        contents = self._fetch_document(document=document)

        if not data:
            data = EnergyData()

        contents.update(data)

        res = requests.put(f"{self.base_url}/{db}/{document}",
                           data=json.dumps(contents),
                           auth=(self.username, self.password))

        return res.ok

    def create_document(self, name: str = None, *, initial_data: EnergyData = None, db: str = None) -> str:
        """Creates a new document named `name`, initialized with `initial_data`.
        Returns the name of the document if creation was successful, and an empty
        string otherwise.

        name -- The name of the document to be created. If omitted, a new UUID
        will be auto-generated and assigned.
        initial_data -- The initial data that will be contained in the created document. initial_data should be
        of-type EnergyData. If omitted, an empty EnergyData object will be used.
        db -- Specified database name. If omitted, the default database name in the config.cfg file will be used.
        """

        # If no name is provided, generate a new UUID on the fly
        if not name:
            res = requests.get(f"{self.base_url}/_uuids")
            name = res.json()["uuids"][0]

        if not db:
            db = self.db

        # Empty bodied requests cannot create new CouchDB Documents.
        # Make sure no empty data are sent.
        if not initial_data:
            initial_data = EnergyData()

        res = requests.put(f"{self.base_url}/{db}/{name}",
                           auth=(self.username, self.password),
                           data=initial_data.as_json(string=True))

        if not res.ok:
            name = ""

        return name

    def delete_document(self, name: str, db: str = None) -> bool:
        data = self._fetch_document(document=name)
        if "_rev" in data:
            rev = data["_rev"]
            if not db:
                db = self.db
            res = requests.delete(f"{self.base_url}/{db}/{name}",
                                  auth=(self.username, self.password),
                                  params={"rev": rev})
            return res.ok

        return False

    def create_database(self, name: str) -> str:
        """Creates a new database named `name`
        Returns the name of the database if creation was successful, and an empty string otherwise.

        name -- The name of the database to be created. If an empty string is given, no database will be created.
        """

        # If no name is provided, no database will be created
        if not name:
            name = ""

        else:
            res = requests.put(f"{self.base_url}/{name}",
                               auth=(self.username, self.password))

            if not res.ok:
                name = ""

        return name

    def delete_database(self, name: str) -> bool:
        """Deletes the database named `name`
        Returns the name of the database if deletion was successful, and an empty string otherwise.

        name -- The name of the existing database to be deleted. If an empty string is given, no database
        will be deleted.
        """
        if name:
            res = requests.delete(f"{self.base_url}/{name}",
                                  auth=(self.username, self.password))
            return res.ok

        return False

    def fetch_energy_data(self, *, document: str, db: str = None) -> EnergyData:
        """Fetches the default document.
        Returns its content as a valid EnergyData object. If operation is unsuccessful, an empty EnergyData object will
         be returned.

        document -- The document to be fetched. It is usually omitted as the
                    default document is being implied, but an arbitrary document
                    can be specified as well.
        db -- The database name/ the id of the device.
        Throws:
        AssertionError -- If no document can be found.
        """

        energy_data = EnergyData()
        data = self._fetch_document(document=document, db=db)

        if data:
            if "date" in data:
                energy_data.date = data["date"]
            if "energy_data" in data:
                energy_data.energy_data = data["energy_data"]

        return energy_data

    def append_energy_data(self, *energy_data_list: EnergyData, document) -> bool:
        """Accepts one or more EnergyData objects and appends their contents to the specified document.
        """

        old_energy_data = self.fetch_energy_data(document=document)

        for energy_data in energy_data_list:
            new_data = energy_data.energy_data

            old_energy_data.energy_data.extend(new_data)

        return self._update_document(old_energy_data.as_json(string=False), document=document)

    def get_document_id_for_date(self, date: str, db: str = None) -> str:
        """Returns the id of the document that matches the given date. If there
        is no such information available on the database, there are no
        appropriate views defined, or there is just no such matching date, an
        empty string will be returned.
        """
        if not db:
            db = self.db
        res = requests.get(f"{self.base_url}/{db}/_design/api/_view/get_dates",
                           auth=(self.username, self.password))

        data = {}
        if res.ok:
            data = res.json()

        rows = []
        if "rows" in data:
            rows = data["rows"]

        document_id = ""
        for row in rows:
            if row["key"] == date:
                document_id = row["value"]
                break

        return document_id

    def fetch_energy_data_by_date(self, date: str, db: str = None) -> EnergyData:
        energy_data = EnergyData()
        doc = self.get_document_id_for_date(date, db=db)
        if doc:
            energy_data = self.fetch_energy_data(document=doc, db=db)
        return energy_data

    def update_energy_data_by_date(self, date: str, data: EnergyData, db: str = None) -> bool:
        if not data:
            data = EnergyData()

        doc = self.get_document_id_for_date(date, db=db)
        if doc:
            contents = self._fetch_document(document=doc, db=db)
            contents["energy_data"] = data.energy_data
            return self._update_document(contents, document=doc, db=db)
        else:
            return bool(self.create_document(initial_data=data, db=db))

    def create_raw_document(self, name: str, *, initial_data: Dict = None, db: str = None) -> str:
        """Creates a new document with arbitrary data named `name`, initialized with `initial_data`.
        Returns the name of the document if creation was successful, and an empty
        string otherwise.

        name -- The name of the document to be created.
        will be auto-generated and assigned.
        initial_data -- The initial data that will be contained in the created document, which MUST be json-serializable
        """

        # If no name is provided, generate a new UUID on the fly
        if name:

            # Empty bodied requests cannot create new CouchDB Documents.
            # Make sure no empty data are sent.
            if not initial_data:
                initial_data = {}
            if not db:
                db = self.db
            res = requests.put(f"{self.base_url}/{db}/{name}",
                               auth=(self.username, self.password),
                               data=json.dumps(initial_data))

            if not res.ok:
                name = ""

        return name

    def fetch_meta(self, db: str = None):
        meta = self._fetch_document(document="meta", db=db)
        meta.pop("_id", None)
        meta.pop("_rev", None)
        return meta

    def update_meta(self, field: str, value: bool | int | float | str | None, db: str = None):
        meta = self._fetch_document(document="meta", db=db)
        meta[field] = value
        from jsonschema import validate
        validate(instance=meta, schema=json_utils.schemas.schema_meta)

        res = requests.put(f"{self.base_url}/{db}/{'meta'}",
                           data=json.dumps(meta),
                           auth=(self.username, self.password))

        return res.ok
