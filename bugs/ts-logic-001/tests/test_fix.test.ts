import { expect, test } from 'vitest'
import { isEven } from '../buggy'

test('2 is even', () => { expect(isEven(2)).toBe(true) })
test('3 is not even', () => { expect(isEven(3)).toBe(false) })
test('0 is even', () => { expect(isEven(0)).toBe(true) })
test('7 is not even', () => { expect(isEven(7)).toBe(false) })
test('100 is even', () => { expect(isEven(100)).toBe(true) })
