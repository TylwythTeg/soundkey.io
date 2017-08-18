from STree import STree
from Chord import Chord

class FingerprintTree():

    @staticmethod
    def replace_sharps(string):
        #print(string)
        normalized = ""
        for note in string:
            normalized += FingerprintTree.normalize_note(note)
        return normalized
    
    @staticmethod
    def sharpify_string(string):
        sharpified = ""
        for note in string:
            sharpified += FingerprintTree.sharpify_note(note)
        return sharpified

    @staticmethod
    def normalize_note(note):
        normalizations = {
            "A": "A",
            "A#": "S",### A Sharp = S
            "S": "S",
            "B": "B",
            "C": "C",
            "C#": "T",### C Sharp = T
            "T": "T",
            "D": "D",
            "D#": "U",### D Sharp = U
            "U": "U",
            "E": "E",
            "F": "F",
            "F#": "V",### F Sharp = V
            "V": "V",
            "G": "G",
            "G#": "W",### G SHarp = W
            "W": "W",
        }
        return normalizations.get(note)

    @staticmethod
    def sharpify_note(note):
        sharpifications = {
            "A": "A",
            "S": "A#",### A Sharp = S
            "B": "B",
            "C": "C",
            "T": "C#",### C Sharp = T
            "D": "D",
            "U": "D#",### D Sharp = U
            "E": "E",
            "F": "F",
            "V": "F#",### F Sharp = V
            "G": "G",
            "W": "G#",### G SHarp = W
        }
        return sharpifications.get(note)

    def __init__(self):

        stamp_list = []
        #####Chord Fingerprints
        for chord in Chord.all():
            #print(chord.notes, chord.name)
            stamp = chord.stamp
            #get a list of the note strings
            stamp = stamp.split(",")
            #replace sharps with single-char equivalents
            stamp = FingerprintTree.replace_sharps(stamp)


            if stamp not in stamp_list:
                stamp_list.append(stamp)

        self.tree = STree(stamp_list)



    def is_terminal(self, char):
        valid_chars = {
            "A": False,
            "S": False,### A Sharp = S
            "B": False,
            "C": False,
            "T": False,### C Sharp = T
            "D": False,
            "U": False,### D Sharp = U
            "E": False,
            "F": False,
            "V": False,### F Sharp = V
            "G": False,
            "W": False,### G SHarp = W
        }
        return valid_chars.get(char, True)

    
    def superstrings(self, y):
        print(y)
        y = FingerprintTree.replace_sharps(y)
        y_input = y
        node = self.tree.root
        while True:
            edge = self.tree._edgeLabel(node, node.parent)
            if edge.startswith(y):
                break
            else:
                i = 0
                while(i < len(edge) and edge[i] == y[0]):
                    y = y[1:]
                    i += 1
            node = node._get_transition_link(y[0])
            if not node:
                return []
        leaves = node._get_leaves()
        return [self.full_stamp_from_index(n.idx) for n in leaves]

    
    #input an index to fing the full string for that index
    def coordinates_from_index(self,index):        
        start = self.get_beginning(index)
        end = self.get_end(index)
 
        return (start, end)
    #get the string at coordinates
    def stamp_from_coordinates(self, coords):
        return self.tree.word[coords[0] : coords[1]]

    def full_stamp_from_index(self, index):
        coords = self.coordinates_from_index(index)
        stamp = self.stamp_from_coordinates(coords)
        return stamp

    def get_beginning(self, index):
        #no footprint would be more than 12 characters in length, and we just want to scan a small part
        word = self.tree.word[index - 12 : index]
        #reverse it so we can trawl it backwards
        word = word[::-1]

        i = 0
        for char in word:
            if self.is_terminal(char):
                break
            i += 1

        beginning = index - i
        return beginning

    def get_end(self, index):

        #no footprint would be more than 12 characters in length, and we just want to scan a small part
        word = self.tree.word[index:index + 12]

        i = 0
        for char in word:
            if self.is_terminal(char):
                break
            i += 1

        end = index + i
        return end









ft = FingerprintTree()

####this is for singular *my* footprint
#print("44444444444444",ft.get_full_index("CEGW"))

print(len(ft.tree.word))
print(ft.stamp_from_coordinates((12,15)))




#get em
superstrings = ft.superstrings("ATE")

print("Normalized:", superstrings)

#convert to real notes
superstrings = [FingerprintTree.sharpify_string(stamp) for stamp in superstrings]

print("\n Human Readable", superstrings)


