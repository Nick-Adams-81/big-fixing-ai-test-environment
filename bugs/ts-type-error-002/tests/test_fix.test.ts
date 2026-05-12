import { expect, test } from 'vitest'
import { countTruthy } from '../buggy'

test('counts truthy values', () => { expect(countTruthy([1, 0, 'a', '', null, true])).toBe(3) })
test('all truthy', () => { expect(countTruthy([1, 2, 3])).toBe(3) })
test('all falsy', () => { expect(countTruthy([0, null, false, ''])).toBe(0) })
test('empty array', () => { expect(countTruthy([])).toBe(0) })
test('mixed booleans', () => { expect(countTruthy([true, false, true])).toBe(2) })
