import collections
import copy
import json
import subprocess


class VersionDict(collections.MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        print "VersionDict.__init__()"
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys
        self.private_head = "private"
        self.public_head = "public"

        self.construct_node(self.public_head)
        self.construct_node(self.private_head, self.add_private_node())

    def __getitem__(self, key):
        return self.store[self.public_head][key]

    def __setitem__(self, key, value):
        self.store[self.public_head][key] = value

    def __delitem__(self, key):
        del self.store[self.public_head][key]

    def __iter__(self):
        return iter(self.store[self.public_head])

    def __len__(self):
        return len(self.store[self.public_head])

    def __str__(self):
        return str(self.store[self.public_head])

    def __repr__(self):
        return self.store[self.public_head]

    def construct_node(self, head_key, tree=None):
        if tree is None:
            self.store[head_key] = {}
        else:
            self.store[head_key] = tree

    def add_private_node(self):
        node = {}
        node["version"] = 0
        return node

    def get_private(self):
        return self.store[self.private_head]

    def deepcopy(self, dictionary):
        self.store = copy.deepcopy(dictionary)


class SanjiConfig(VersionDict):
    """A dictionary that applies Sanji's format."""
    def __init__(self, file_path):
        super(SanjiConfig, self).__init__()
        print "SanjiConfig.__init__()"

        self.file_path = file_path
        self.load(self.file_path)

    def load(self, file_path=None):
        if file_path is None:
            file_path = self.file_path

        with open(file_path, "r") as db_file:
            raw_json = json.load(db_file)

        try:
            self.store["public"] = raw_json["public"]
        except KeyError:
            self.construct_node(self.public_head, raw_json)

        try:
            self.store["private"] = raw_json["private"]
        except KeyError:
            self.construct_node(self.private_head)

    def save(self, file_path=None):
        if file_path is None:
            file_path = self.file_path

        with open(file_path, "w") as db_file:
            json.dump(self.store, db_file, indent=4)

        cmd = "sync"
        subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    '''
    s = VersionDict()
    s['Test'] = 5
    s['Bat'] = "Yang"

    print s

    A = dict()
    A['private'] = dict()
    A['private']['version'] = 300
    A['private']['obj'] = dict()
    A['private']['obj']['name'] = "John"
    A['public'] = dict()
    A['public']['ip'] = "192.168.31.254"

    cc = VersionDict()
    cc.deepcopy(A)
    private = cc.get_private()
    print private
    private["obj"]["name"] = "Matt"
    print cc

    print "-" * 80
    sanji_config = SanjiConfig("./model.json")
    sanji_config.save()

    print sanji_config
    '''
    pass
