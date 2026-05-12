import { expect, test } from 'vitest'
import { abs } from '../buggy'

test('positive stays positive', () => { expect(abs(5)).toBe(5) })
test('negative becomes positive', () => { expect(abs(-3)).toBe(3) })
test('zero stays zero', () => { expect(abs(0)).toBe(0) })
test('abs(-10) = 10', () => { expect(abs(-10)).toBe(10) })
test('abs(7) = 7', () => { expect(abs(7)).toBe(7) })
