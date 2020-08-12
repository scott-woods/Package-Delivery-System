class PackageHashTable:

    # Creates a Nested Array as a Hash Table
    # Runs in O(N)
    def __init__(self, size=10):
        self.size = size
        self.hashTable = []
        for i in range(size):
            self.hashTable.append([])

    # Insert new Key Value Pair
    # Runs in O(1)
    def insert(self, key, value):
        bucket = self.getBucket(key)
        keyValuePair = [key, value]
        self.hashTable[bucket].append(keyValuePair)

    # Update the Value of a Key Value Pair given the Key
    # Runs in O(N)
    def update(self, key, value):
        bucket = self.getBucket(key)
        if self.hashTable[bucket] is not None:
            for pair in self.hashTable[bucket]:
                if pair[0] == key:
                    pair[1] = value

    # Search for Package Info by Key
    # Runs in O(N)
    def search(self, key):
        bucket = self.getBucket(key)
        bucketList = self.hashTable[bucket]
        for pair in bucketList:
            if pair[0] == key:
                value = pair[1]
                return value

    # Delete a row by Key
    # Runs in O(N)
    def delete(self, key):
        bucket = self.getBucket(key)
        bucketList = self.hashTable[bucket]
        if bucketList is None:
            return False
        for pair in bucketList:
            if pair[0] == key:
                index = bucketList.index(pair)
                bucketList.pop(index)
                return True
        return False

    # Hash function returns Bucket given Key
    # Runs in O(1)
    def getBucket(self, key):
        bucket = int(key) % len(self.hashTable)
        return bucket
