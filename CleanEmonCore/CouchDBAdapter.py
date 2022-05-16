"""Database-related communication module"""

import configparser
import json

import requests

from .models import EnergyData


class CouchDBAdapter:
    """ChouchDB Adapter class used to exchange data using REST API."""

    def __init__(self, config_file: str):

        # Load configuration file
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(config_file)

        self.endpoint = cfg["DB"]["endpoint"]
        self.db = cfg["DB"]["db_name"]
        self.document = cfg["DB"]["document_name"]
        self.username = cfg["DB"]["username"]
        self.password = cfg["DB"]["password"]
        self.base_url = f"{self.endpoint}"

    def _fetch_document(self, *, document: str = None) -> dict:
        """Fetches the default document.
        Returns its content in json-format. If operation is unsuccessful, an
        empty dict is being returned.

        document -- The document to be fetched. It is usually omitted as the
                    default document is being implied, but an arbitrary document
                    can be specified as well.

        Throws:
        AssertionError -- If no document can be found.
        """

        if not document:
            document = self.document

        assert document, "No document was supplied!"

        res = requests.get(f"{self.base_url}/{self.db}/{document}",
                           auth=(self.username, self.password))

        data = {}

        if res.ok:
            data = res.json()

        return data

    def _update_document(self, data: dict, *, document=None) -> bool:
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

        if not document:
            document = self.document

        assert document, "No document was supplied!"

        contents = self._fetch_document(document=document)

        if not data:
            data = EnergyData()

        contents.update(data)

        res = requests.put(f"{self.base_url}/{self.db}/{document}",
                           data=json.dumps(contents),
                           auth=(self.username, self.password))

        return res.ok

    def create_document(self, name: str = None, *, initial_data: EnergyData = None) -> str:
        """Creates a new document named `name`, initialized with `initial_data`.
        Returns the name of the document if creation was successful, and an empty
        string otherwise.

        name -- The name of the document to be created. If omitted, a new UUID
        will be auto-generated and assigned.
        initial_data -- The initial data that will be contained in the created document. initial_data should be
        of-type EnergyData. If omitted, an empty EnergyData object will be used.
        """

        # If no name is provided, generate a new UUID on the fly
        if not name:
            res = requests.get(f"{self.base_url}/_uuids")
            name = res.json()["uuids"][0]

        # Empty bodied requests cannot create new CouchDB Documents.
        # Make sure no empty data are sent.
        if not initial_data:
            initial_data = EnergyData()

        res = requests.put(f"{self.base_url}/{self.db}/{name}",
                           auth=(self.username, self.password),
                           data=initial_data.as_json(string=True))

        if not res.ok:
            name = ""

        return name

    def delete_document(self, name: str) -> bool:
        data = self._fetch_document(document=name)
        if "_rev" in data:
            rev = data["_rev"]
            res = requests.delete(f"{self.base_url}/{self.db}/{name}",
                                  auth=(self.username, self.password),
                                  params={"rev": rev})
            return res.ok

        return False

    def fetch_energy_data(self, *, document: str = None) -> EnergyData:
        """Fetches the default document.
        Returns its content as a valid EnergyData object. If operation is unsuccessful, an empty EnergyData object will
         be returned.

        document -- The document to be fetched. It is usually omitted as the
                    default document is being implied, but an arbitrary document
                    can be specified as well.

        Throws:
        AssertionError -- If no document can be found.
        """

        energy_data = EnergyData()
        data = self._fetch_document(document=document)

        if data:
            if "date" in data:
                energy_data.date = data["date"]
            if "energy_data" in data:
                energy_data.energy_data = data["energy_data"]

        return energy_data

    def append_energy_data(self, energy_data: EnergyData, *, document=None) -> bool:
        """Accepts an EnergyData object and appends its contents to the specified document.
        """

        new_data = energy_data.energy_data

        copy = self.fetch_energy_data(document=document)
        copy.energy_data.extend(new_data)

        return self._update_document(copy.as_json(string=False), document=document)

    def get_document_id_for_date(self, date: str) -> str:
        """Returns the id of the document that matches the given date. If there
        is no such information available on the database, there are no
        appropriate views defined, or there is just no such matching date, an
        empty string will be returned.
        """

        res = requests.get(f"{self.base_url}/{self.db}/_design/api/_view/get_dates",
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

    def fetch_energy_data_by_date(self, date: str) -> EnergyData:
        energy_data = EnergyData()
        doc = self.get_document_id_for_date(date)
        if doc:
            energy_data = self.fetch_energy_data(document=doc)
        return energy_data

    def update_energy_data_by_date(self, date: str, data: EnergyData) -> bool:
        if not data:
            data = EnergyData()

        doc = self.get_document_id_for_date(date)
        if doc:
            contents = self._fetch_document(document=doc)
            contents["energy_data"] = data.energy_data
            return self._update_document(contents, document=doc)
        else:
            return bool(self.create_document(initial_data=data))
