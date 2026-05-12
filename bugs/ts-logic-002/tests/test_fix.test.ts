import { expect, test } from 'vitest'
import { clamp } from '../buggy'

test('in range returns value', () => { expect(clamp(5, 0, 10)).toBe(5) })
test('at min returns min', () => { expect(clamp(0, 0, 10)).toBe(0) })
test('at max returns max', () => { expect(clamp(10, 0, 10)).toBe(10) })
test('below min returns min', () => { expect(clamp(-1, 0, 10)).toBe(0) })
test('above max returns max', () => { expect(clamp(11, 0, 10)).toBe(10) })
