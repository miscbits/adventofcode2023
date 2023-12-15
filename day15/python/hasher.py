class Label:
    """docstring for Label"""

    def __init__(self, text):
        self.value = 0
        if "=" in text:
            self.text, self.value = text.split("=")
            self.value = int(self.value)
            self.additive = True
        elif "-" in text:
            self.text = text[:-1]
            self.additive = False
        else:
            self.text = text
            self.additive = False

    def __hash__(self):
        hash_val = 0
        for c in self.text:
            hash_val = ((hash_val + ord(c)) * 17) % 256
        return hash_val

    def __eq__(self, other):
        return self.text == other.text

    def __str__(self):
        return f"[{self.text} {str(self.value)}]"


class AsciiHashMap:
    """docstring for AsciiHashMap"""

    def __init__(self):
        self.boxes = []
        for i in range(256):
            self.boxes.append([])

    def add_label(self, label: Label):
        label_hash = hash(label)
        if label in self.boxes[label_hash]:
            self.boxes[label_hash][self.boxes[label_hash].index(label)] = label
        else:
            self.boxes[label_hash].append(label)

    def remove_label(self, label):
        label_hash = hash(label)
        if label in self.boxes[label_hash]:
            self.boxes[label_hash].remove(label)

    def get_focal_length(self):
        focal_length = 0
        for ib, box in enumerate(self.boxes):
            for il, label in enumerate(box):
                focal_length += (ib + 1) * (il + 1) * label.value
        return focal_length

    def __str__(self):
        str_rep = ""
        for i, box in [(i, x) for i, x in enumerate(self.boxes) if len(x)]:
            str_rep += (
                "Box " + str(i) + " " + " ".join([str(label) for label in box]) + "\n"
            )
        return str_rep


def hash_256(string: str) -> int:
    hash_val = 0
    for c in string:
        hash_val = ((hash_val + ord(c)) * 17) % 256
    return hash_val


def part_1():
    with open("../input.txt") as input_file:
        hashed_values = map(hash_256, input_file.read().split(","))
    return sum(hashed_values)


def part_2():
    ascii_hashmap = AsciiHashMap()
    with open("../input.txt") as input_file:
        labels = [Label(x) for x in input_file.read().split(",")]
    for label in labels:
        if label.additive:
            ascii_hashmap.add_label(label)
        else:
            ascii_hashmap.remove_label(label)
    return ascii_hashmap.get_focal_length()


if __name__ == "__main__":
    print(part_1())
    print(part_2())
