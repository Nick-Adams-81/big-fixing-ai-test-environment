import { expect, test } from 'vitest'
import { repeat } from '../buggy'

test('repeat "ab" 3 times', () => { expect(repeat('ab', 3)).toBe('ababab') })
test('repeat once', () => { expect(repeat('hi', 1)).toBe('hi') })
test('repeat zero times', () => { expect(repeat('x', 0)).toBe('') })
test('repeat "a" 5 times', () => { expect(repeat('a', 5)).toBe('aaaaa') })
