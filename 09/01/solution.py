import argparse

def get_solution(input_path):
    with open(input_path) as input_file:
        result = []
        nums = input_file.readline().strip()
        file_data = [int(x) for x in nums[::2]]
        empty_data = [int(x) for x in nums[1::2]]
        left = 0
        right = len(file_data) - 1

        while left < right:
            for i in range(file_data[left]):
                result.append(left)

            # Shifting file data left is a little more complicated since we may have to pull from
            # more than one "bucket" (decrement the right index in the middle of the operation)
            # depending on how many empty spaces we have to fill.
            while left < right and empty_data[left] > 0:
                if file_data[right] == 0:
                    right -= 1
                else:
                    result.append(right)
                    empty_data[left] -= 1
                    file_data[right] -= 1

            left += 1

        for i in range(file_data[left]):
            result.append(left)

        return sum([i * x for i, x in enumerate(result)])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
