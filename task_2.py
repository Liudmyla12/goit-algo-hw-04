from typing import List


def merge_two(a: List[int], b: List[int]) -> List[int]:
    res = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    res.extend(a[i:])
    res.extend(b[j:])
    return res


def merge_k_lists(lists: List[List[int]]) -> List[int]:
    """
    Об'єднує k відсортованих списків у один відсортований список.
    Реалізація: злиття попарно (divide & conquer).
    """
    if not lists:
        return []

    current = lists[:]
    while len(current) > 1:
        merged = []
        for i in range(0, len(current), 2):
            if i + 1 < len(current):
                merged.append(merge_two(current[i], current[i + 1]))
            else:
                merged.append(current[i])
        current = merged
    return current[0]


if __name__ == "__main__":
    lists_ = [[1, 4, 5], [1, 3, 4], [2, 6]]
    merged_list = merge_k_lists(lists_)
    print("Відсортований список:", merged_list)
