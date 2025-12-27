import argparse
import random
import timeit
from typing import Callable, List, Dict


def insertion_sort(data: List[int]) -> List[int]:
    arr = data[:]  # працюємо з копією
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge(left: List[int], right: List[int]) -> List[int]:
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res


def merge_sort(data: List[int]) -> List[int]:
    arr = data[:]  # копія
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def timsort(data: List[int]) -> List[int]:
    # Вбудоване сортування Python (Timsort). sorted() не змінює оригінал
    return sorted(data)


def make_dataset(n: int, kind: str, seed: int = 42) -> List[int]:
    rng = random.Random(seed)

    if kind == "random":
        return [rng.randint(0, 10**6) for _ in range(n)]

    if kind == "sorted":
        return list(range(n))

    if kind == "reversed":
        return list(range(n, 0, -1))

    if kind == "nearly_sorted":
        arr = list(range(n))
        # робимо ~1% випадкових swap, щоб список був "майже" відсортований
        swaps = max(1, n // 100)
        for _ in range(swaps):
            i = rng.randrange(n)
            j = rng.randrange(n)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    raise ValueError(f"Unknown dataset kind: {kind}")


def measure(func: Callable[[List[int]], List[int]], data: List[int], repeat: int = 5) -> float:
    timer = timeit.Timer(lambda: func(data))
    times = timer.repeat(repeat=repeat, number=1)
    return min(times)


def run_benchmarks(
    sizes: List[int],
    kinds: List[str],
    repeat: int
) -> Dict[str, Dict[int, Dict[str, float]]]:
    algorithms = {
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Timsort (built-in)": timsort,
    }

    results: Dict[str, Dict[int, Dict[str, float]]] = {}

    for kind in kinds:
        results[kind] = {}
        for n in sizes:
            data = make_dataset(n, kind=kind)

            # перевірка коректності (один раз на датасет)
            expected = sorted(data)
            assert insertion_sort(data) == expected
            assert merge_sort(data) == expected
            assert timsort(data) == expected

            results[kind][n] = {}
            for name, func in algorithms.items():
                # Insertion Sort стає дуже повільним на великих n — обмежимо розумно
                if name == "Insertion Sort" and n > 5000:
                    results[kind][n][name] = float("nan")
                    continue
                results[kind][n][name] = measure(func, data, repeat=repeat)
    return results


def print_results(results: Dict[str, Dict[int, Dict[str, float]]]) -> None:
    for kind, by_size in results.items():
        print("\n" + "=" * 72)
        print(f"DATASET: {kind}")
        print("=" * 72)
        print("| Size | Insertion Sort | Merge Sort | Timsort (built-in) |")
        print("|------|----------------|-----------|--------------------|")
        for n, row in by_size.items():
            ins = row.get("Insertion Sort", float("nan"))
            ms = row.get("Merge Sort", float("nan"))
            ts = row.get("Timsort (built-in)", float("nan"))

            def fmt(x: float) -> str:
                return "—" if x != x else f"{x:.6f}"  # NaN -> —
            print(f"| {n:<4} | {fmt(ins):<14} | {fmt(ms):<9} | {fmt(ts):<18} |")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare Merge Sort, Insertion Sort and Timsort using timeit."
    )
    parser.add_argument(
        "--sizes",
        default="1000,2000,5000",
        help="Comma-separated list sizes (default: 1000,2000,5000)",
    )
    parser.add_argument(
        "--kinds",
        default="random,sorted,reversed,nearly_sorted",
        help="Comma-separated dataset kinds: random,sorted,reversed,nearly_sorted",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=5,
        help="timeit repeats (default: 5)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    sizes = [int(x.strip()) for x in args.sizes.split(",") if x.strip()]
    kinds = [x.strip() for x in args.kinds.split(",") if x.strip()]
    repeat = args.repeat

    results = run_benchmarks(sizes=sizes, kinds=kinds, repeat=repeat)
    print_results(results)

    print("\nВисновок (коротко):")
    print("- Timsort (built-in) зазвичай найшвидший на практиці.")
    print("- Insertion Sort нормальний на майже відсортованих даних, але повільний на великих масивах.")
    print("- Merge Sort стабільний (O(n log n)), але часто програє Timsort через оптимізації вбудованого сортування.")


if __name__ == "__main__":
    main()
