import { expect, test } from 'vitest'
import { divide } from '../buggy'

test('10 / 2 = 5', () => { expect(divide(10, 2)).toBe(5) })
test('9 / 3 = 3', () => { expect(divide(9, 3)).toBe(3) })
test('7 / 1 = 7', () => { expect(divide(7, 1)).toBe(7) })
test('0 / 5 = 0', () => { expect(divide(0, 5)).toBe(0) })
test('1 / 4 = 0.25', () => { expect(divide(1, 4)).toBe(0.25) })
