class ListDict:

    def __init__(self):
        self.storage = []

    def insert(self, word):
        word = word.lower()
        try:
            self.storage.index(word)
        except ValueError:
            self.storage.append(word)

    def lookup(self, word):
        word = word.lower()
        try:
            self.storage.index(word)
            return True
        except ValueError:
            return False

class HashMapDict:

    def __init__(self):
        self.storage = {}

    def insert(self, word):
        word = word.lower()
        self.storage[word] = True

    def lookup(self, word):
        word = word.lower()
        return True if self.storage.get(word, False) else False

class BinarySearchTreeDict:

    class Node:
        def __init__(self, left, word, right):
            self.left = left
            self.word = word
            self.right = right

    def __init__(self):
        self.storage = None

    def insert(self, word):
        print "inserting: ", word
        self.storage = self._insert(word.lower(), self.storage)

    def _insert(self, word, node):
        if ( node == None ):
            return self.Node(None, word, None)
        elif ( word < node.word ):
            return self.Node(self._insert(word, node.left),
                node.word, node.right)
        elif ( word > node.word ):
            return self.Node(node.left,
                node.word, self._insert(word, node.right))
        else:
            return self.Node(node.left, node.word, node.right)

    def lookup(self, word):
        return self._lookup(word.lower(), self.storage)

    def _lookup(self, word, node):
        if ( node == None ):
            return False
        elif ( word < node.word ):
            return self._lookup(word, node.left)
        elif ( word > node.word ):
            return self._lookup(word, node.right)
        else:
            return True

if __name__ == "__main__":

    import sys, time, resource as res, os

    if ( len(sys.argv) != 4 ):
        print ( "Format should be:\n\n" +
            "$./execute.sh <data_structure> <data_file> <queries_file>" )
        exit(1)

    data_structure_key = sys.argv[1]
    if ( data_structure_key == "binarytree" ):
        data_structure = BinarySearchTreeDict()
    elif ( data_structure_key == "hashmap" ):
        data_structure = HashMapDict()
    elif ( data_structure_key == "list" ):
        data_structure = ListDict()
    else:
        print ( "Invalid data structure key " +
            "{}, aborting.".format(data_structure_key) )
        exit(1)

    data_file = sys.argv[2]
    if ( not os.path.exists(data_file) ):
        print "{} doesn't exist, aborting.".format(data_file)
        exit(1)
    data_file = open(data_file, 'r')

    words = []
    for word in data_file.readlines():
        words.append(word.strip())

    start = time.clock()
    for word in words:
        data_structure.insert(word)
    insertion_time = time.clock() - start

    queries_file = sys.argv[3]
    if ( not os.path.exists(queries_file) ):
        print "{} doesn't exist, aborting.".format(queries_file)
        exit(1)
    queries_file = open(queries_file, 'r')

    words = []
    for word in queries_file.readlines():
        words.append(word.strip())

    results = []
    start = time.clock()
    for word in words:
        results.append(data_structure.lookup(word))
    lookup_time = time.clock() - start

    for i in range(len(words)):
        print '<{}>: {}'.format(words[i],
            "S" if results[i] else "N")
    print "tempo_de_carga: {} segundos".format(insertion_time)
    print "tempo_da_consulta: {} segundos".format(lookup_time)
    process = res.RUSAGE_SELF
    memory_consumption = res.getrusage(process).ru_maxrss
    memory_consumption *= res.getpagesize()
    memory_consumption /= 1048576.0
    print "consumo_de_memoria: {} MB".format(memory_consumption)