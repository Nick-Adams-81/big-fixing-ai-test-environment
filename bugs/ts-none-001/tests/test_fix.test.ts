import { expect, test } from 'vitest'
import { getLength } from '../buggy'

test('returns length of array', () => { expect(getLength(['a', 'b', 'c'])).toBe(3) })
test('returns 0 for null', () => { expect(getLength(null)).toBe(0) })
test('returns 0 for empty array', () => { expect(getLength([])).toBe(0) })
test('returns 1 for single element', () => { expect(getLength(['x'])).toBe(1) })
