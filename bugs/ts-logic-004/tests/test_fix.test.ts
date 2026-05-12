import { expect, test } from 'vitest'
import { fibonacci } from '../buggy'

test('fib(0) = 0', () => { expect(fibonacci(0)).toBe(0) })
test('fib(1) = 1', () => { expect(fibonacci(1)).toBe(1) })
test('fib(2) = 1', () => { expect(fibonacci(2)).toBe(1) })
test('fib(5) = 5', () => { expect(fibonacci(5)).toBe(5) })
test('fib(7) = 13', () => { expect(fibonacci(7)).toBe(13) })
