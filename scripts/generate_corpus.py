#!/usr/bin/env python3
"""Generate Phase 6 corpus expansion: 40 new bugs across Python, TypeScript, and Go."""
import difflib
import json
from pathlib import Path

BUGS_DIR = Path("bugs")

CONFTEST_PY = """import sys
from pathlib import Path
sys.modules.pop("buggy", None)
sys.path.insert(0, str(Path(__file__).parent.parent))
"""


def make_patch(filename, buggy, fixed):
    diff = difflib.unified_diff(
        buggy.splitlines(keepends=True),
        fixed.splitlines(keepends=True),
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
    )
    return "".join(diff)


def py_bug(bug_id, category, difficulty, description, buggy_code, fixed_code, test_code):
    d = BUGS_DIR / bug_id
    d.mkdir(exist_ok=True)
    (d / "buggy.py").write_text(buggy_code)
    (d / "metadata.json").write_text(json.dumps({
        "id": bug_id, "language": "python", "category": category,
        "difficulty": difficulty, "description": description, "entrypoint": "buggy.py",
    }, indent=2) + "\n")
    (d / "solution.patch").write_text(make_patch("buggy.py", buggy_code, fixed_code))
    td = d / "tests"
    td.mkdir(exist_ok=True)
    (td / "conftest.py").write_text(CONFTEST_PY)
    (td / "test_fix.py").write_text(test_code)
    print(f"  {bug_id}")


def ts_bug(bug_id, category, difficulty, description, buggy_code, fixed_code, test_code):
    d = BUGS_DIR / bug_id
    d.mkdir(exist_ok=True)
    (d / "buggy.ts").write_text(buggy_code)
    (d / "metadata.json").write_text(json.dumps({
        "id": bug_id, "language": "typescript", "category": category,
        "difficulty": difficulty, "description": description, "entrypoint": "buggy.ts",
    }, indent=2) + "\n")
    (d / "solution.patch").write_text(make_patch("buggy.ts", buggy_code, fixed_code))
    td = d / "tests"
    td.mkdir(exist_ok=True)
    (td / "test_fix.test.ts").write_text(test_code)
    print(f"  {bug_id}")


def go_bug(bug_id, category, difficulty, description, buggy_code, fixed_code, test_code):
    d = BUGS_DIR / bug_id
    d.mkdir(exist_ok=True)
    (d / "buggy.go").write_text(buggy_code)
    (d / "buggy_test.go").write_text(test_code)
    (d / "go.mod").write_text("module buggy\n\ngo 1.21\n")
    (d / "metadata.json").write_text(json.dumps({
        "id": bug_id, "language": "go", "category": category,
        "difficulty": difficulty, "description": description, "entrypoint": "buggy.go",
    }, indent=2) + "\n")
    (d / "solution.patch").write_text(make_patch("buggy.go", buggy_code, fixed_code))
    print(f"  {bug_id}")


# ── PYTHON BUGS ──────────────────────────────────────────────────────────────

print("Python:")

py_bug("py-off-by-one-004", "off-by-one", "easy",
    "Slice returns n-1 elements instead of n.",
    buggy_code="""\
def first_n(items: list, n: int) -> list:
    \"\"\"Return the first n elements of items.\"\"\"
    return items[:n - 1]
""",
    fixed_code="""\
def first_n(items: list, n: int) -> list:
    \"\"\"Return the first n elements of items.\"\"\"
    return items[:n]
""",
    test_code="""\
from buggy import first_n


def test_first_three():
    assert first_n([1, 2, 3, 4, 5], 3) == [1, 2, 3]


def test_first_one():
    assert first_n([10, 20, 30], 1) == [10]


def test_first_all():
    lst = [1, 2, 3]
    assert first_n(lst, 3) == lst


def test_first_two():
    assert first_n(list(range(10)), 2) == [0, 1]


def test_zero():
    assert first_n([1, 2, 3], 0) == []
""")

py_bug("py-off-by-one-005", "off-by-one", "easy",
    "Loop repeats n-1 times instead of n.",
    buggy_code="""\
def repeat_str(s: str, n: int) -> str:
    \"\"\"Return string s repeated n times.\"\"\"
    result = ""
    for _ in range(n - 1):
        result += s
    return result
""",
    fixed_code="""\
def repeat_str(s: str, n: int) -> str:
    \"\"\"Return string s repeated n times.\"\"\"
    result = ""
    for _ in range(n):
        result += s
    return result
""",
    test_code="""\
from buggy import repeat_str


def test_repeat_three():
    assert repeat_str("ab", 3) == "ababab"


def test_repeat_once():
    assert repeat_str("hi", 1) == "hi"


def test_repeat_zero():
    assert repeat_str("x", 0) == ""


def test_repeat_five():
    assert repeat_str("a", 5) == "aaaaa"


def test_repeat_empty():
    assert repeat_str("", 4) == ""
""")

py_bug("py-logic-006", "logic", "easy",
    "clamp returns lo instead of value when in range.",
    buggy_code="""\
def clamp(value: float, lo: float, hi: float) -> float:
    \"\"\"Clamp value to the range [lo, hi].\"\"\"
    if value < lo:
        return lo
    if value > hi:
        return hi
    return lo
""",
    fixed_code="""\
def clamp(value: float, lo: float, hi: float) -> float:
    \"\"\"Clamp value to the range [lo, hi].\"\"\"
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value
""",
    test_code="""\
from buggy import clamp


def test_in_range():
    assert clamp(5.0, 0.0, 10.0) == 5.0


def test_at_lo():
    assert clamp(0.0, 0.0, 10.0) == 0.0


def test_at_hi():
    assert clamp(10.0, 0.0, 10.0) == 10.0


def test_below_lo():
    assert clamp(-1.0, 0.0, 10.0) == 0.0


def test_above_hi():
    assert clamp(11.0, 0.0, 10.0) == 10.0
""")

py_bug("py-logic-007", "logic", "easy",
    "count_divisible uses != instead of ==.",
    buggy_code="""\
def count_divisible(numbers: list, divisor: int) -> int:
    \"\"\"Return count of numbers evenly divisible by divisor.\"\"\"
    return sum(1 for n in numbers if n % divisor != 0)
""",
    fixed_code="""\
def count_divisible(numbers: list, divisor: int) -> int:
    \"\"\"Return count of numbers evenly divisible by divisor.\"\"\"
    return sum(1 for n in numbers if n % divisor == 0)
""",
    test_code="""\
from buggy import count_divisible


def test_divisible_by_2():
    assert count_divisible([1, 2, 3, 4, 6], 2) == 3


def test_divisible_by_3():
    assert count_divisible([3, 6, 9, 10], 3) == 3


def test_none_divisible():
    assert count_divisible([1, 2, 4], 3) == 0


def test_all_divisible():
    assert count_divisible([4, 8, 12], 4) == 3


def test_empty():
    assert count_divisible([], 5) == 0
""")

py_bug("py-type-error-002", "type-error", "easy",
    "total_length sums the strings themselves instead of their lengths.",
    buggy_code="""\
def total_length(strings: list) -> int:
    \"\"\"Return total character count across all strings.\"\"\"
    return sum(strings)
""",
    fixed_code="""\
def total_length(strings: list) -> int:
    \"\"\"Return total character count across all strings.\"\"\"
    return sum(len(s) for s in strings)
""",
    test_code="""\
import pytest
from buggy import total_length


def test_basic():
    assert total_length(["hello", "world"]) == 10


def test_single():
    assert total_length(["abc"]) == 3


def test_empty_list():
    assert total_length([]) == 0


def test_empty_strings():
    assert total_length(["", "", ""]) == 0


def test_mixed():
    assert total_length(["a", "bb", "ccc"]) == 6
""")

py_bug("py-type-error-003", "type-error", "easy",
    "is_positive compares x to string '0' instead of int 0.",
    buggy_code="""\
def is_positive(x) -> bool:
    \"\"\"Return True if x is a positive number.\"\"\"
    return x > "0"
""",
    fixed_code="""\
def is_positive(x) -> bool:
    \"\"\"Return True if x is a positive number.\"\"\"
    return x > 0
""",
    test_code="""\
import pytest
from buggy import is_positive


def test_positive():
    assert is_positive(5) is True


def test_negative():
    assert is_positive(-3) is False


def test_zero():
    assert is_positive(0) is False


def test_float():
    assert is_positive(0.1) is True


def test_large():
    assert is_positive(1000) is True
""")

py_bug("py-none-002", "null-dereference", "easy",
    "get_value calls .strip() on None when key is missing.",
    buggy_code="""\
def get_value(d: dict, key: str) -> str:
    \"\"\"Return stripped value for key, or empty string if not found.\"\"\"
    value = d.get(key)
    return value.strip()
""",
    fixed_code="""\
def get_value(d: dict, key: str) -> str:
    \"\"\"Return stripped value for key, or empty string if not found.\"\"\"
    value = d.get(key)
    return value.strip() if value is not None else ""
""",
    test_code="""\
import pytest
from buggy import get_value


def test_existing_key():
    assert get_value({"name": "  Alice  "}, "name") == "Alice"


def test_missing_key():
    assert get_value({}, "name") == ""


def test_no_whitespace():
    assert get_value({"x": "hello"}, "x") == "hello"


def test_whitespace_only():
    assert get_value({"x": "   "}, "x") == ""
""")

py_bug("py-none-003", "null-dereference", "easy",
    "safe_first tries to index an empty list instead of returning None.",
    buggy_code="""\
def safe_first(lst: list):
    \"\"\"Return the first element, or None if the list is empty.\"\"\"
    if len(lst) > 0:
        return lst[0]
    return lst[0]
""",
    fixed_code="""\
def safe_first(lst: list):
    \"\"\"Return the first element, or None if the list is empty.\"\"\"
    if len(lst) > 0:
        return lst[0]
    return None
""",
    test_code="""\
import pytest
from buggy import safe_first


def test_non_empty():
    assert safe_first([1, 2, 3]) == 1


def test_empty():
    assert safe_first([]) is None


def test_single():
    assert safe_first([42]) == 42


def test_strings():
    assert safe_first(["a", "b"]) == "a"
""")

py_bug("py-logic-008", "logic", "medium",
    "max_subarray_sum returns current_sum instead of max_sum.",
    buggy_code="""\
def max_subarray_sum(numbers: list) -> int:
    \"\"\"Return the maximum sum of any contiguous subarray (Kadane's algorithm).\"\"\"
    max_sum = numbers[0]
    current_sum = numbers[0]
    for num in numbers[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return current_sum
""",
    fixed_code="""\
def max_subarray_sum(numbers: list) -> int:
    \"\"\"Return the maximum sum of any contiguous subarray (Kadane's algorithm).\"\"\"
    max_sum = numbers[0]
    current_sum = numbers[0]
    for num in numbers[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum
""",
    test_code="""\
from buggy import max_subarray_sum


def test_all_positive():
    assert max_subarray_sum([1, 2, 3, 4]) == 10


def test_mixed():
    assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6


def test_all_negative():
    assert max_subarray_sum([-3, -1, -2]) == -1


def test_single():
    assert max_subarray_sum([5]) == 5


def test_reset():
    assert max_subarray_sum([3, -10, 4]) == 4
""")

py_bug("py-logic-009", "logic", "medium",
    "rotate_right performs a left rotation instead of right.",
    buggy_code="""\
def rotate_right(lst: list, k: int) -> list:
    \"\"\"Rotate list right by k positions.\"\"\"
    if not lst:
        return lst
    k = k % len(lst)
    return lst[k:] + lst[:k]
""",
    fixed_code="""\
def rotate_right(lst: list, k: int) -> list:
    \"\"\"Rotate list right by k positions.\"\"\"
    if not lst:
        return lst
    k = k % len(lst)
    return lst[-k:] + lst[:-k]
""",
    test_code="""\
from buggy import rotate_right


def test_rotate_by_1():
    assert rotate_right([1, 2, 3, 4, 5], 1) == [5, 1, 2, 3, 4]


def test_rotate_by_2():
    assert rotate_right([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]


def test_rotate_by_0():
    assert rotate_right([1, 2, 3], 0) == [1, 2, 3]


def test_empty():
    assert rotate_right([], 3) == []


def test_full_rotation():
    lst = [1, 2, 3]
    assert rotate_right(lst, 3) == lst
""")


# ── TYPESCRIPT BUGS ──────────────────────────────────────────────────────────

print("TypeScript:")

ts_bug("ts-off-by-one-001", "off-by-one", "easy",
    "firstN slices n-1 elements instead of n.",
    buggy_code="""\
export function firstN<T>(arr: T[], n: number): T[] {
    return arr.slice(0, n - 1);
}
""",
    fixed_code="""\
export function firstN<T>(arr: T[], n: number): T[] {
    return arr.slice(0, n);
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { firstN } from '../buggy'

test('returns first 3 elements', () => {
    expect(firstN([1, 2, 3, 4, 5], 3)).toEqual([1, 2, 3])
})

test('returns first 1 element', () => {
    expect(firstN([10, 20, 30], 1)).toEqual([10])
})

test('returns all elements', () => {
    expect(firstN([1, 2, 3], 3)).toEqual([1, 2, 3])
})

test('returns first 2', () => {
    expect(firstN([0, 1, 2, 3, 4], 2)).toEqual([0, 1])
})

test('returns empty for n=0', () => {
    expect(firstN([1, 2, 3], 0)).toEqual([])
})
""")

ts_bug("ts-off-by-one-002", "off-by-one", "easy",
    "sumUpTo uses i < n so it skips the last value.",
    buggy_code="""\
export function sumUpTo(n: number): number {
    let total = 0;
    for (let i = 1; i < n; i++) {
        total += i;
    }
    return total;
}
""",
    fixed_code="""\
export function sumUpTo(n: number): number {
    let total = 0;
    for (let i = 1; i <= n; i++) {
        total += i;
    }
    return total;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { sumUpTo } from '../buggy'

test('sum 1..5 = 15', () => {
    expect(sumUpTo(5)).toBe(15)
})

test('sum 1..1 = 1', () => {
    expect(sumUpTo(1)).toBe(1)
})

test('sum 1..10 = 55', () => {
    expect(sumUpTo(10)).toBe(55)
})

test('sum 1..0 = 0', () => {
    expect(sumUpTo(0)).toBe(0)
})

test('sum 1..3 = 6', () => {
    expect(sumUpTo(3)).toBe(6)
})
""")

ts_bug("ts-off-by-one-003", "off-by-one", "easy",
    "lastN returns one fewer element than requested.",
    buggy_code="""\
export function lastN<T>(arr: T[], n: number): T[] {
    return arr.slice(arr.length - n - 1);
}
""",
    fixed_code="""\
export function lastN<T>(arr: T[], n: number): T[] {
    return arr.slice(arr.length - n);
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { lastN } from '../buggy'

test('last 3 of 5', () => {
    expect(lastN([1, 2, 3, 4, 5], 3)).toEqual([3, 4, 5])
})

test('last 1', () => {
    expect(lastN([10, 20, 30], 1)).toEqual([30])
})

test('last 2', () => {
    expect(lastN([1, 2, 3, 4], 2)).toEqual([3, 4])
})

test('all elements', () => {
    expect(lastN([1, 2, 3], 3)).toEqual([1, 2, 3])
})
""")

ts_bug("ts-logic-001", "logic", "easy",
    "isEven checks remainder equals 1 instead of 0.",
    buggy_code="""\
export function isEven(n: number): boolean {
    return n % 2 === 1;
}
""",
    fixed_code="""\
export function isEven(n: number): boolean {
    return n % 2 === 0;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { isEven } from '../buggy'

test('2 is even', () => { expect(isEven(2)).toBe(true) })
test('3 is not even', () => { expect(isEven(3)).toBe(false) })
test('0 is even', () => { expect(isEven(0)).toBe(true) })
test('7 is not even', () => { expect(isEven(7)).toBe(false) })
test('100 is even', () => { expect(isEven(100)).toBe(true) })
""")

ts_bug("ts-logic-002", "logic", "easy",
    "clamp returns min instead of value when value is in range.",
    buggy_code="""\
export function clamp(value: number, min: number, max: number): number {
    if (value < min) return min;
    if (value > max) return max;
    return min;
}
""",
    fixed_code="""\
export function clamp(value: number, min: number, max: number): number {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { clamp } from '../buggy'

test('in range returns value', () => { expect(clamp(5, 0, 10)).toBe(5) })
test('at min returns min', () => { expect(clamp(0, 0, 10)).toBe(0) })
test('at max returns max', () => { expect(clamp(10, 0, 10)).toBe(10) })
test('below min returns min', () => { expect(clamp(-1, 0, 10)).toBe(0) })
test('above max returns max', () => { expect(clamp(11, 0, 10)).toBe(10) })
""")

ts_bug("ts-logic-003", "logic", "easy",
    "abs returns negative of positive numbers and vice versa.",
    buggy_code="""\
export function abs(n: number): number {
    return n < 0 ? n : -n;
}
""",
    fixed_code="""\
export function abs(n: number): number {
    return n < 0 ? -n : n;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { abs } from '../buggy'

test('positive stays positive', () => { expect(abs(5)).toBe(5) })
test('negative becomes positive', () => { expect(abs(-3)).toBe(3) })
test('zero stays zero', () => { expect(abs(0)).toBe(0) })
test('abs(-10) = 10', () => { expect(abs(-10)).toBe(10) })
test('abs(7) = 7', () => { expect(abs(7)).toBe(7) })
""")

ts_bug("ts-logic-004", "logic", "medium",
    "fibonacci recurses with n-3 instead of n-2.",
    buggy_code="""\
export function fibonacci(n: number): number {
    if (n <= 0) return 0;
    if (n === 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 3);
}
""",
    fixed_code="""\
export function fibonacci(n: number): number {
    if (n <= 0) return 0;
    if (n === 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { fibonacci } from '../buggy'

test('fib(0) = 0', () => { expect(fibonacci(0)).toBe(0) })
test('fib(1) = 1', () => { expect(fibonacci(1)).toBe(1) })
test('fib(2) = 1', () => { expect(fibonacci(2)).toBe(1) })
test('fib(5) = 5', () => { expect(fibonacci(5)).toBe(5) })
test('fib(7) = 13', () => { expect(fibonacci(7)).toBe(13) })
""")

ts_bug("ts-logic-005", "logic", "easy",
    "divide has its arguments swapped.",
    buggy_code="""\
export function divide(a: number, b: number): number {
    return b / a;
}
""",
    fixed_code="""\
export function divide(a: number, b: number): number {
    return a / b;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { divide } from '../buggy'

test('10 / 2 = 5', () => { expect(divide(10, 2)).toBe(5) })
test('9 / 3 = 3', () => { expect(divide(9, 3)).toBe(3) })
test('7 / 1 = 7', () => { expect(divide(7, 1)).toBe(7) })
test('0 / 5 = 0', () => { expect(divide(0, 5)).toBe(0) })
test('1 / 4 = 0.25', () => { expect(divide(1, 4)).toBe(0.25) })
""")

ts_bug("ts-type-error-001", "type-error", "easy",
    "repeat appends the count n instead of the string s.",
    buggy_code="""\
export function repeat(s: string, n: number): string {
    let result = '';
    for (let i = 0; i < n; i++) {
        result += n;
    }
    return result;
}
""",
    fixed_code="""\
export function repeat(s: string, n: number): string {
    let result = '';
    for (let i = 0; i < n; i++) {
        result += s;
    }
    return result;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { repeat } from '../buggy'

test('repeat "ab" 3 times', () => { expect(repeat('ab', 3)).toBe('ababab') })
test('repeat once', () => { expect(repeat('hi', 1)).toBe('hi') })
test('repeat zero times', () => { expect(repeat('x', 0)).toBe('') })
test('repeat "a" 5 times', () => { expect(repeat('a', 5)).toBe('aaaaa') })
""")

ts_bug("ts-type-error-002", "type-error", "easy",
    "countTruthy filters falsy values instead of truthy ones.",
    buggy_code="""\
export function countTruthy(arr: unknown[]): number {
    return arr.filter(x => !x).length;
}
""",
    fixed_code="""\
export function countTruthy(arr: unknown[]): number {
    return arr.filter(x => Boolean(x)).length;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { countTruthy } from '../buggy'

test('counts truthy values', () => { expect(countTruthy([1, 0, 'a', '', null, true])).toBe(3) })
test('all truthy', () => { expect(countTruthy([1, 2, 3])).toBe(3) })
test('all falsy', () => { expect(countTruthy([0, null, false, ''])).toBe(0) })
test('empty array', () => { expect(countTruthy([])).toBe(0) })
test('mixed booleans', () => { expect(countTruthy([true, false, true])).toBe(2) })
""")

ts_bug("ts-none-001", "null-dereference", "easy",
    "getLength accesses .length without checking for null.",
    buggy_code="""\
export function getLength(arr: string[] | null): number {
    return arr.length;
}
""",
    fixed_code="""\
export function getLength(arr: string[] | null): number {
    return arr ? arr.length : 0;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { getLength } from '../buggy'

test('returns length of array', () => { expect(getLength(['a', 'b', 'c'])).toBe(3) })
test('returns 0 for null', () => { expect(getLength(null)).toBe(0) })
test('returns 0 for empty array', () => { expect(getLength([])).toBe(0) })
test('returns 1 for single element', () => { expect(getLength(['x'])).toBe(1) })
""")

ts_bug("ts-none-002", "null-dereference", "easy",
    "greet calls toUpperCase on name without checking for undefined.",
    buggy_code="""\
export function greet(name: string | undefined): string {
    return `Hello, ${name.toUpperCase()}!`;
}
""",
    fixed_code="""\
export function greet(name: string | undefined): string {
    return `Hello, ${(name ?? 'World').toUpperCase()}!`;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { greet } from '../buggy'

test('greets by name', () => { expect(greet('alice')).toBe('Hello, ALICE!') })
test('falls back to World for undefined', () => { expect(greet(undefined)).toBe('Hello, WORLD!') })
test('uppercases name', () => { expect(greet('bob')).toBe('Hello, BOB!') })
""")

ts_bug("ts-logic-006", "logic", "easy",
    "unique keeps duplicates instead of removing them.",
    buggy_code="""\
export function unique<T>(arr: T[]): T[] {
    return arr.filter((item, index) => arr.indexOf(item) !== index);
}
""",
    fixed_code="""\
export function unique<T>(arr: T[]): T[] {
    return arr.filter((item, index) => arr.indexOf(item) === index);
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { unique } from '../buggy'

test('removes duplicates', () => { expect(unique([1, 2, 2, 3, 3, 3])).toEqual([1, 2, 3]) })
test('no duplicates unchanged', () => { expect(unique([1, 2, 3])).toEqual([1, 2, 3]) })
test('all duplicates', () => { expect(unique([5, 5, 5])).toEqual([5]) })
test('empty array', () => { expect(unique([])).toEqual([]) })
test('strings', () => { expect(unique(['a', 'b', 'a'])).toEqual(['a', 'b']) })
""")

ts_bug("ts-logic-007", "logic", "medium",
    "factorial uses addition instead of multiplication.",
    buggy_code="""\
export function factorial(n: number): number {
    if (n <= 1) return 1;
    return n + factorial(n - 1);
}
""",
    fixed_code="""\
export function factorial(n: number): number {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { factorial } from '../buggy'

test('0! = 1', () => { expect(factorial(0)).toBe(1) })
test('1! = 1', () => { expect(factorial(1)).toBe(1) })
test('3! = 6', () => { expect(factorial(3)).toBe(6) })
test('5! = 120', () => { expect(factorial(5)).toBe(120) })
test('4! = 24', () => { expect(factorial(4)).toBe(24) })
""")

ts_bug("ts-logic-008", "logic", "medium",
    "max3 returns a in the final else branch instead of c.",
    buggy_code="""\
export function max3(a: number, b: number, c: number): number {
    if (a >= b && a >= c) return a;
    if (b >= a && b >= c) return b;
    return a;
}
""",
    fixed_code="""\
export function max3(a: number, b: number, c: number): number {
    if (a >= b && a >= c) return a;
    if (b >= a && b >= c) return b;
    return c;
}
""",
    test_code="""\
import { expect, test } from 'vitest'
import { max3 } from '../buggy'

test('c is largest', () => { expect(max3(1, 2, 3)).toBe(3) })
test('a is largest', () => { expect(max3(9, 3, 5)).toBe(9) })
test('b is largest', () => { expect(max3(2, 8, 4)).toBe(8) })
test('all equal', () => { expect(max3(5, 5, 5)).toBe(5) })
test('c ties with b', () => { expect(max3(1, 7, 7)).toBe(7) })
""")


# ── GO BUGS ──────────────────────────────────────────────────────────────────

print("Go:")

go_bug("go-off-by-one-001", "off-by-one", "easy",
    "FirstN returns n-1 elements instead of n.",
    buggy_code="""\
package buggy

func FirstN(s []int, n int) []int {
\treturn s[:n-1]
}
""",
    fixed_code="""\
package buggy

func FirstN(s []int, n int) []int {
\treturn s[:n]
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestFirstNThree(t *testing.T) {
\tgot := buggy.FirstN([]int{1, 2, 3, 4, 5}, 3)
\twant := []int{1, 2, 3}
\tif len(got) != len(want) {
\t\tt.Errorf("FirstN returned %v, want %v", got, want)
\t}
\tfor i := range want {
\t\tif got[i] != want[i] {
\t\t\tt.Errorf("FirstN[%d] = %d, want %d", i, got[i], want[i])
\t\t}
\t}
}

func TestFirstNOne(t *testing.T) {
\tgot := buggy.FirstN([]int{10, 20, 30}, 1)
\tif len(got) != 1 || got[0] != 10 {
\t\tt.Errorf("FirstN returned %v, want [10]", got)
\t}
}

func TestFirstNTwo(t *testing.T) {
\tgot := buggy.FirstN([]int{0, 1, 2, 3}, 2)
\tif len(got) != 2 || got[0] != 0 || got[1] != 1 {
\t\tt.Errorf("FirstN returned %v, want [0 1]", got)
\t}
}

func TestFirstNAll(t *testing.T) {
\ts := []int{1, 2, 3}
\tgot := buggy.FirstN(s, 3)
\tif len(got) != 3 {
\t\tt.Errorf("FirstN returned %v, want %v", got, s)
\t}
}
""")

go_bug("go-off-by-one-002", "off-by-one", "easy",
    "Repeat loops n-1 times instead of n.",
    buggy_code="""\
package buggy

func Repeat(s string, n int) string {
\tresult := ""
\tfor i := 0; i < n-1; i++ {
\t\tresult += s
\t}
\treturn result
}
""",
    fixed_code="""\
package buggy

func Repeat(s string, n int) string {
\tresult := ""
\tfor i := 0; i < n; i++ {
\t\tresult += s
\t}
\treturn result
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestRepeatThree(t *testing.T) {
\tgot := buggy.Repeat("ab", 3)
\tif got != "ababab" {
\t\tt.Errorf("Repeat(ab,3) = %q, want %q", got, "ababab")
\t}
}

func TestRepeatOnce(t *testing.T) {
\tgot := buggy.Repeat("hi", 1)
\tif got != "hi" {
\t\tt.Errorf("Repeat(hi,1) = %q, want %q", got, "hi")
\t}
}

func TestRepeatZero(t *testing.T) {
\tgot := buggy.Repeat("x", 0)
\tif got != "" {
\t\tt.Errorf("Repeat(x,0) = %q, want empty", got)
\t}
}

func TestRepeatFive(t *testing.T) {
\tgot := buggy.Repeat("a", 5)
\tif got != "aaaaa" {
\t\tt.Errorf("Repeat(a,5) = %q, want %q", got, "aaaaa")
\t}
}
""")

go_bug("go-off-by-one-003", "off-by-one", "easy",
    "LastN returns one fewer element than requested.",
    buggy_code="""\
package buggy

func LastN(s []int, n int) []int {
\treturn s[len(s)-n-1:]
}
""",
    fixed_code="""\
package buggy

func LastN(s []int, n int) []int {
\treturn s[len(s)-n:]
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestLastNThree(t *testing.T) {
\tgot := buggy.LastN([]int{1, 2, 3, 4, 5}, 3)
\tif len(got) != 3 || got[0] != 3 || got[1] != 4 || got[2] != 5 {
\t\tt.Errorf("LastN returned %v, want [3 4 5]", got)
\t}
}

func TestLastNOne(t *testing.T) {
\tgot := buggy.LastN([]int{10, 20, 30}, 1)
\tif len(got) != 1 || got[0] != 30 {
\t\tt.Errorf("LastN returned %v, want [30]", got)
\t}
}

func TestLastNTwo(t *testing.T) {
\tgot := buggy.LastN([]int{1, 2, 3, 4}, 2)
\tif len(got) != 2 || got[0] != 3 || got[1] != 4 {
\t\tt.Errorf("LastN returned %v, want [3 4]", got)
\t}
}

func TestLastNAll(t *testing.T) {
\ts := []int{1, 2, 3}
\tgot := buggy.LastN(s, 3)
\tif len(got) != 3 {
\t\tt.Errorf("LastN returned %v, want %v", got, s)
\t}
}
""")

go_bug("go-logic-001", "logic", "easy",
    "IsEven checks remainder equals 1 instead of 0.",
    buggy_code="""\
package buggy

func IsEven(n int) bool {
\treturn n%2 == 1
}
""",
    fixed_code="""\
package buggy

func IsEven(n int) bool {
\treturn n%2 == 0
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestIsEven2(t *testing.T) {
\tif !buggy.IsEven(2) { t.Error("2 should be even") }
}

func TestIsEven3(t *testing.T) {
\tif buggy.IsEven(3) { t.Error("3 should not be even") }
}

func TestIsEven0(t *testing.T) {
\tif !buggy.IsEven(0) { t.Error("0 should be even") }
}

func TestIsEven7(t *testing.T) {
\tif buggy.IsEven(7) { t.Error("7 should not be even") }
}

func TestIsEven100(t *testing.T) {
\tif !buggy.IsEven(100) { t.Error("100 should be even") }
}
""")

go_bug("go-logic-002", "logic", "easy",
    "Clamp returns lo instead of value when value is in range.",
    buggy_code="""\
package buggy

func Clamp(value, lo, hi float64) float64 {
\tif value < lo {
\t\treturn lo
\t}
\tif value > hi {
\t\treturn hi
\t}
\treturn lo
}
""",
    fixed_code="""\
package buggy

func Clamp(value, lo, hi float64) float64 {
\tif value < lo {
\t\treturn lo
\t}
\tif value > hi {
\t\treturn hi
\t}
\treturn value
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestClampInRange(t *testing.T) {
\tif got := buggy.Clamp(5, 0, 10); got != 5 {
\t\tt.Errorf("Clamp(5,0,10) = %v, want 5", got)
\t}
}

func TestClampAtLo(t *testing.T) {
\tif got := buggy.Clamp(0, 0, 10); got != 0 {
\t\tt.Errorf("Clamp(0,0,10) = %v, want 0", got)
\t}
}

func TestClampAtHi(t *testing.T) {
\tif got := buggy.Clamp(10, 0, 10); got != 10 {
\t\tt.Errorf("Clamp(10,0,10) = %v, want 10", got)
\t}
}

func TestClampBelowLo(t *testing.T) {
\tif got := buggy.Clamp(-1, 0, 10); got != 0 {
\t\tt.Errorf("Clamp(-1,0,10) = %v, want 0", got)
\t}
}

func TestClampAboveHi(t *testing.T) {
\tif got := buggy.Clamp(11, 0, 10); got != 10 {
\t\tt.Errorf("Clamp(11,0,10) = %v, want 10", got)
\t}
}
""")

go_bug("go-logic-003", "logic", "easy",
    "Abs returns n unchanged when n is negative.",
    buggy_code="""\
package buggy

func Abs(n int) int {
\tif n < 0 {
\t\treturn n
\t}
\treturn n
}
""",
    fixed_code="""\
package buggy

func Abs(n int) int {
\tif n < 0 {
\t\treturn -n
\t}
\treturn n
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestAbsPositive(t *testing.T) {
\tif got := buggy.Abs(5); got != 5 {
\t\tt.Errorf("Abs(5) = %d, want 5", got)
\t}
}

func TestAbsNegative(t *testing.T) {
\tif got := buggy.Abs(-3); got != 3 {
\t\tt.Errorf("Abs(-3) = %d, want 3", got)
\t}
}

func TestAbsZero(t *testing.T) {
\tif got := buggy.Abs(0); got != 0 {
\t\tt.Errorf("Abs(0) = %d, want 0", got)
\t}
}

func TestAbsNegTen(t *testing.T) {
\tif got := buggy.Abs(-10); got != 10 {
\t\tt.Errorf("Abs(-10) = %d, want 10", got)
\t}
}
""")

go_bug("go-logic-004", "logic", "medium",
    "Fibonacci recurses with n-3 instead of n-2.",
    buggy_code="""\
package buggy

func Fibonacci(n int) int {
\tif n <= 0 {
\t\treturn 0
\t}
\tif n == 1 {
\t\treturn 1
\t}
\treturn Fibonacci(n-1) + Fibonacci(n-3)
}
""",
    fixed_code="""\
package buggy

func Fibonacci(n int) int {
\tif n <= 0 {
\t\treturn 0
\t}
\tif n == 1 {
\t\treturn 1
\t}
\treturn Fibonacci(n-1) + Fibonacci(n-2)
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestFib0(t *testing.T) {
\tif got := buggy.Fibonacci(0); got != 0 { t.Errorf("Fibonacci(0) = %d, want 0", got) }
}

func TestFib1(t *testing.T) {
\tif got := buggy.Fibonacci(1); got != 1 { t.Errorf("Fibonacci(1) = %d, want 1", got) }
}

func TestFib2(t *testing.T) {
\tif got := buggy.Fibonacci(2); got != 1 { t.Errorf("Fibonacci(2) = %d, want 1", got) }
}

func TestFib5(t *testing.T) {
\tif got := buggy.Fibonacci(5); got != 5 { t.Errorf("Fibonacci(5) = %d, want 5", got) }
}

func TestFib7(t *testing.T) {
\tif got := buggy.Fibonacci(7); got != 13 { t.Errorf("Fibonacci(7) = %d, want 13", got) }
}
""")

go_bug("go-logic-005", "logic", "easy",
    "Divide returns b/a instead of a/b.",
    buggy_code="""\
package buggy

func Divide(a, b float64) float64 {
\treturn b / a
}
""",
    fixed_code="""\
package buggy

func Divide(a, b float64) float64 {
\treturn a / b
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestDivide10by2(t *testing.T) {
\tif got := buggy.Divide(10, 2); got != 5 { t.Errorf("Divide(10,2) = %v, want 5", got) }
}

func TestDivide9by3(t *testing.T) {
\tif got := buggy.Divide(9, 3); got != 3 { t.Errorf("Divide(9,3) = %v, want 3", got) }
}

func TestDivide7by1(t *testing.T) {
\tif got := buggy.Divide(7, 1); got != 7 { t.Errorf("Divide(7,1) = %v, want 7", got) }
}

func TestDivide1by4(t *testing.T) {
\tif got := buggy.Divide(1, 4); got != 0.25 { t.Errorf("Divide(1,4) = %v, want 0.25", got) }
}

func TestDivide0by5(t *testing.T) {
\tif got := buggy.Divide(0, 5); got != 0 { t.Errorf("Divide(0,5) = %v, want 0", got) }
}
""")

go_bug("go-type-error-001", "type-error", "easy",
    "SumLengths uses len(strs) instead of len(s) inside the loop.",
    buggy_code="""\
package buggy

func SumLengths(strs []string) int {
\ttotal := 0
\tfor _, s := range strs {
\t\ttotal += len(strs)
\t}
\treturn total
}
""",
    fixed_code="""\
package buggy

func SumLengths(strs []string) int {
\ttotal := 0
\tfor _, s := range strs {
\t\ttotal += len(s)
\t}
\treturn total
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestSumLengthsBasic(t *testing.T) {
\tif got := buggy.SumLengths([]string{"hello", "world"}); got != 10 {
\t\tt.Errorf("SumLengths = %d, want 10", got)
\t}
}

func TestSumLengthsSingle(t *testing.T) {
\tif got := buggy.SumLengths([]string{"abc"}); got != 3 {
\t\tt.Errorf("SumLengths = %d, want 3", got)
\t}
}

func TestSumLengthsEmpty(t *testing.T) {
\tif got := buggy.SumLengths([]string{}); got != 0 {
\t\tt.Errorf("SumLengths = %d, want 0", got)
\t}
}

func TestSumLengthsMixed(t *testing.T) {
\tif got := buggy.SumLengths([]string{"a", "bb", "ccc"}); got != 6 {
\t\tt.Errorf("SumLengths = %d, want 6", got)
\t}
}
""")

go_bug("go-nil-001", "null-dereference", "easy",
    "Head panics on an empty slice instead of returning empty string.",
    buggy_code="""\
package buggy

func Head(s []string) string {
\treturn s[0]
}
""",
    fixed_code="""\
package buggy

func Head(s []string) string {
\tif len(s) == 0 {
\t\treturn ""
\t}
\treturn s[0]
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestHeadNonEmpty(t *testing.T) {
\tif got := buggy.Head([]string{"a", "b", "c"}); got != "a" {
\t\tt.Errorf("Head = %q, want %q", got, "a")
\t}
}

func TestHeadEmpty(t *testing.T) {
\tif got := buggy.Head([]string{}); got != "" {
\t\tt.Errorf("Head(empty) = %q, want empty string", got)
\t}
}

func TestHeadSingle(t *testing.T) {
\tif got := buggy.Head([]string{"only"}); got != "only" {
\t\tt.Errorf("Head = %q, want %q", got, "only")
\t}
}
""")

go_bug("go-nil-002", "null-dereference", "easy",
    "Double dereferences a nil pointer instead of returning 0.",
    buggy_code="""\
package buggy

func Double(p *int) int {
\treturn *p * 2
}
""",
    fixed_code="""\
package buggy

func Double(p *int) int {
\tif p == nil {
\t\treturn 0
\t}
\treturn *p * 2
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestDoubleNil(t *testing.T) {
\tif got := buggy.Double(nil); got != 0 {
\t\tt.Errorf("Double(nil) = %d, want 0", got)
\t}
}

func TestDoubleValue(t *testing.T) {
\tv := 5
\tif got := buggy.Double(&v); got != 10 {
\t\tt.Errorf("Double(&5) = %d, want 10", got)
\t}
}

func TestDoubleZero(t *testing.T) {
\tv := 0
\tif got := buggy.Double(&v); got != 0 {
\t\tt.Errorf("Double(&0) = %d, want 0", got)
\t}
}

func TestDoubleNeg(t *testing.T) {
\tv := -3
\tif got := buggy.Double(&v); got != -6 {
\t\tt.Errorf("Double(&-3) = %d, want -6", got)
\t}
}
""")

go_bug("go-logic-006", "logic", "easy",
    "Max returns b when a is larger.",
    buggy_code="""\
package buggy

func Max(a, b int) int {
\tif a > b {
\t\treturn b
\t}
\treturn b
}
""",
    fixed_code="""\
package buggy

func Max(a, b int) int {
\tif a > b {
\t\treturn a
\t}
\treturn b
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestMaxALarger(t *testing.T) {
\tif got := buggy.Max(10, 3); got != 10 { t.Errorf("Max(10,3) = %d, want 10", got) }
}

func TestMaxBLarger(t *testing.T) {
\tif got := buggy.Max(2, 7); got != 7 { t.Errorf("Max(2,7) = %d, want 7", got) }
}

func TestMaxEqual(t *testing.T) {
\tif got := buggy.Max(5, 5); got != 5 { t.Errorf("Max(5,5) = %d, want 5", got) }
}

func TestMaxNeg(t *testing.T) {
\tif got := buggy.Max(-1, -5); got != -1 { t.Errorf("Max(-1,-5) = %d, want -1", got) }
}
""")

go_bug("go-logic-007", "logic", "medium",
    "Factorial uses addition instead of multiplication.",
    buggy_code="""\
package buggy

func Factorial(n int) int {
\tif n <= 1 {
\t\treturn 1
\t}
\treturn n + Factorial(n-1)
}
""",
    fixed_code="""\
package buggy

func Factorial(n int) int {
\tif n <= 1 {
\t\treturn 1
\t}
\treturn n * Factorial(n-1)
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestFactorial0(t *testing.T) {
\tif got := buggy.Factorial(0); got != 1 { t.Errorf("Factorial(0) = %d, want 1", got) }
}

func TestFactorial1(t *testing.T) {
\tif got := buggy.Factorial(1); got != 1 { t.Errorf("Factorial(1) = %d, want 1", got) }
}

func TestFactorial3(t *testing.T) {
\tif got := buggy.Factorial(3); got != 6 { t.Errorf("Factorial(3) = %d, want 6", got) }
}

func TestFactorial5(t *testing.T) {
\tif got := buggy.Factorial(5); got != 120 { t.Errorf("Factorial(5) = %d, want 120", got) }
}

func TestFactorial4(t *testing.T) {
\tif got := buggy.Factorial(4); got != 24 { t.Errorf("Factorial(4) = %d, want 24", got) }
}
""")

go_bug("go-off-by-one-004", "off-by-one", "medium",
    "Contains stops one element short, missing the last element.",
    buggy_code="""\
package buggy

func Contains(s []int, target int) bool {
\tfor i := 0; i < len(s)-1; i++ {
\t\tif s[i] == target {
\t\t\treturn true
\t\t}
\t}
\treturn false
}
""",
    fixed_code="""\
package buggy

func Contains(s []int, target int) bool {
\tfor i := 0; i < len(s); i++ {
\t\tif s[i] == target {
\t\t\treturn true
\t\t}
\t}
\treturn false
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestContainsLast(t *testing.T) {
\tif !buggy.Contains([]int{1, 2, 3, 4, 5}, 5) {
\t\tt.Error("Contains should find last element 5")
\t}
}

func TestContainsFirst(t *testing.T) {
\tif !buggy.Contains([]int{1, 2, 3}, 1) {
\t\tt.Error("Contains should find first element 1")
\t}
}

func TestContainsMid(t *testing.T) {
\tif !buggy.Contains([]int{10, 20, 30}, 20) {
\t\tt.Error("Contains should find middle element 20")
\t}
}

func TestContainsMissing(t *testing.T) {
\tif buggy.Contains([]int{1, 2, 3}, 9) {
\t\tt.Error("Contains should not find 9")
\t}
}

func TestContainsEmpty(t *testing.T) {
\tif buggy.Contains([]int{}, 1) {
\t\tt.Error("Contains should return false for empty slice")
\t}
}
""")

go_bug("go-logic-008", "logic", "medium",
    "CountOccurrences counts non-matching elements instead of matching ones.",
    buggy_code="""\
package buggy

func CountOccurrences(s []int, target int) int {
\tcount := 0
\tfor _, v := range s {
\t\tif v != target {
\t\t\tcount++
\t\t}
\t}
\treturn count
}
""",
    fixed_code="""\
package buggy

func CountOccurrences(s []int, target int) int {
\tcount := 0
\tfor _, v := range s {
\t\tif v == target {
\t\t\tcount++
\t\t}
\t}
\treturn count
}
""",
    test_code="""\
package buggy_test

import (
\t"buggy"
\t"testing"
)

func TestCountOccurrencesBasic(t *testing.T) {
\tif got := buggy.CountOccurrences([]int{1, 2, 2, 3, 2}, 2); got != 3 {
\t\tt.Errorf("CountOccurrences = %d, want 3", got)
\t}
}

func TestCountOccurrencesNone(t *testing.T) {
\tif got := buggy.CountOccurrences([]int{1, 2, 3}, 9); got != 0 {
\t\tt.Errorf("CountOccurrences = %d, want 0", got)
\t}
}

func TestCountOccurrencesAll(t *testing.T) {
\tif got := buggy.CountOccurrences([]int{5, 5, 5}, 5); got != 3 {
\t\tt.Errorf("CountOccurrences = %d, want 3", got)
\t}
}

func TestCountOccurrencesEmpty(t *testing.T) {
\tif got := buggy.CountOccurrences([]int{}, 1); got != 0 {
\t\tt.Errorf("CountOccurrences = %d, want 0", got)
\t}
}

func TestCountOccurrencesOne(t *testing.T) {
\tif got := buggy.CountOccurrences([]int{1, 2, 3, 4}, 3); got != 1 {
\t\tt.Errorf("CountOccurrences = %d, want 1", got)
\t}
}
""")

print("\nDone. Run: python -m harness.batch --agent passthrough to verify.")
