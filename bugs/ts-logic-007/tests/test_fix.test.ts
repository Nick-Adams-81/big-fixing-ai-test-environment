import { expect, test } from 'vitest'
import { factorial } from '../buggy'

test('0! = 1', () => { expect(factorial(0)).toBe(1) })
test('1! = 1', () => { expect(factorial(1)).toBe(1) })
test('3! = 6', () => { expect(factorial(3)).toBe(6) })
test('5! = 120', () => { expect(factorial(5)).toBe(120) })
test('4! = 24', () => { expect(factorial(4)).toBe(24) })
