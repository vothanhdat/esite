class ArrayWrapper:
    def __init__(self, generator):
        self.generator = generator
        self.array = []
        self.index = 0

    def __getitem__(self, key):
        if key not in self.array:
            for x in range(self.index, key + 1):
                self.array[x] = self.generator.next()
        return self.array[key]

    def __contains__(self, key):
        return key in self.array
    
    def __iter__(self):
        return self.array.__iter__()
