import hashlib
import json


class Merkleroot(object):
    def __init__(self):
        pass

    def doubleSha256(input):
        return hashlib.sha256(hashlib.sha256(input).hexdigest()).hexdigest()

    def findMerkleRoot(self, leafHash):
        hash = []
        hash2 = []
        if len(leafHash) % 2 != 0:
            leafHash.extend(leafHash[-1:])

        for leaf in sorted(leafHash):
            hash.append(leaf)
            if len(hash) % 2 == 0:

                hash2.append(doubleSha256(hash[0]+hash[1]))
                hash == []
        if len(hash2) == 1:
            return hash2
        else:
            return self.findMerkleRoot(hash2)


def doubleSha256(input):
    return hashlib.sha256(hashlib.sha256(input.encode()).hexdigest().encode()).hexdigest()


def get_merkle_tree_hash(block_string):

    data = []

    try:
        with open('data.json') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print()

    transactions = data
    leafHash = []

    if len(data) > 0:
        for trans in transactions:
            json_trans = json.dumps(trans, sort_keys=True)
            leafHash.append(doubleSha256(json_trans))

        mr = Merkleroot()
        c_hash = mr.findMerkleRoot(leafHash)[0]

        return c_hash
    else:
        # print('block_string')
        return doubleSha256(block_string)
