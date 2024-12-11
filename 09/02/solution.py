import argparse
from itertools import batched

class Slot():
    def __init__(self, file_id, file_size, empty_data):
        self.prefix_empty = 0
        self.file_data = [{'id': file_id, 'size': file_size}]
        self.trailing_empty = empty_data

    def get_raw_layout(self):
        # Yeah this ain't pretty. Basically we need a list of integers representing the raw layout of
        # this single slot, so any empty prefix blocks followed by any file blocks followed by any
        # trailing empty space.
        return ([0] * self.prefix_empty
                + [block for blocks in map(lambda s: [s['id']] * s['size'], self.file_data) for block in blocks]
                + [0] * self.trailing_empty)

def do_compression(slots):
    for i in range(len(slots) - 1, 0, -1):
        right = slots[i]
        swap_candidate = right.file_data[0]
        for j in range(0, i):
            left = slots[j]
            if left.trailing_empty >= swap_candidate['size']:
                left.file_data.append(swap_candidate)
                left.trailing_empty -= swap_candidate['size']
                right.file_data = right.file_data[1:]
                right.prefix_empty += swap_candidate['size']
                break

def get_solution(input_path):
    with open(input_path) as input_file:
        raw_input = [int(x) for x in input_file.readline().strip()]
        # Pad with an extra 0 if it's an odd number of ints so that the batching operation has
        # enough data to work with
        raw_input += [0] * (len(raw_input) % 2)
        slots = [Slot(file_id, file_size, empty_data) for (file_id, (file_size, empty_data)) in enumerate(batched(raw_input, 2))]
        do_compression(slots)
        raw_disk_layout = [item for sublist in [slot.get_raw_layout() for slot in slots] for item in sublist]
        return sum([i * val for i, val in enumerate(raw_disk_layout)])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
