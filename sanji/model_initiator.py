#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os
import shutil
import subprocess


class ModelInitiator(object):
    """
    "   Deal with some model initialization works like DB
    "   and Condifuration files creating.
    """
    def __init__(self, model_name, model_path, db_type="json"):
        self.model_name = model_name
        self.model_path = model_path
        self.db = None
        self.data_folder_path = self.model_path + "/data"
        self.factory_json_db_path = self.model_path + "/data/" + \
            self.model_name + ".factory.json"
        self.json_db_path = self.model_path + "/data/" + \
            self.model_name + ".json"
        self.db_type = db_type

        self.create_db()
        self.load_db()

    def create_db(self):
        """
        "   Create a db file for model if there is no db.
        "   User need to prepare thier own xxx.factory.json.
        """
        self.factory_json_db_path = self.model_path + "/data/" + \
            self.model_name + ".factory.json"
        self.json_db_path = self.model_path + "/data/" + \
            self.model_name + ".json"

        if self.db_type == "json":
            if not os.path.exists(self.json_db_path):
                if os.path.exists(self.factory_json_db_path):
                    shutil.copy2(self.factory_json_db_path, self.json_db_path)
                    return True
                else:
                    print "*** NO: " + self.factory_json_db_path

        return False

    def load_db(self):
        """
        " Load json db as a dictionary.
        """
        try:
            with open(self.json_db_path) as fp:
                self.db = json.load(fp)
        except Exception:
            print "*** Open JSON DB error."

    def save_db(self):
        """
        " Save json db to file system.
        """
        try:
            with open(self.json_db_path, "w") as fp:
                json.dump(self.db, fp, indent=4)
        except Exception:
            print "*** Write JSON DB to file error."
        else:
            self.sync()

    def sync(self):
        """
        " Call Linux 'sync' command to write data from RAM to flash.
        """
        cmd = "sync"
        subprocess.call(cmd, shell=True)

    def __del__(self):
        pass
