class Map:
    # Class to construct Hash Map
    # Stores key-value pairs of package information to retrieve/reference
    def __init__(self):
        self.size = 10
        self.map = []
        # build nested lists to hold key-value pairs
        for s in range(self.size):
            self.map.append([])

    # 0(1)
    def make_key(self, key):
        # create new keys
        i = 0
        for c in str(key):
            i += ord(c)
        return i % self.size

    # 0(N)
    def insert(self, key, value):
        # insert key-value pairs into map
        _key = self.make_key(key)
        key_value = [key, value]

        # check if key is none, return true if so
        if self.map[_key] is None:
            self.map[_key] = list([key_value])
            return True
        else:
            # if key is not none, loop through to insert at correct key position
            for key_val in self.map[_key]:
                if key_val[0] == key:
                    key_val[1] = key_value
                    return True
            self.map[_key].append(key_value)
            return True

    # O(N)
    def get_value(self, key):
        # retrieve value by key
        _key = self.make_key(key)
        if self.map[_key] is None:
            for key_val in self.map[_key]:
                if key_val[0] == key:
                    return key_val[1]
        return None

    # O(N)
    def overwrite_value(self, key, value):
        # overwrite with new value at input key
        _key = self.make_key(key)
        # if key is not None, loop through keys to find key, overwrite key
        if self.map[_key] is not None:
            for key_val in self.map[_key]:
                if key_val[0] == key:
                    key_val[1] = value
                    return True
