import { expect, test } from 'vitest'
import { max3 } from '../buggy'

test('c is largest', () => { expect(max3(1, 2, 3)).toBe(3) })
test('a is largest', () => { expect(max3(9, 3, 5)).toBe(9) })
test('b is largest', () => { expect(max3(2, 8, 4)).toBe(8) })
test('all equal', () => { expect(max3(5, 5, 5)).toBe(5) })
test('c ties with b', () => { expect(max3(1, 7, 7)).toBe(7) })
