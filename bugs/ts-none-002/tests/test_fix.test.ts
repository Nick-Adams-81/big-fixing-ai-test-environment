import { expect, test } from 'vitest'
import { greet } from '../buggy'

test('greets by name', () => { expect(greet('alice')).toBe('Hello, ALICE!') })
test('falls back to World for undefined', () => { expect(greet(undefined)).toBe('Hello, WORLD!') })
test('uppercases name', () => { expect(greet('bob')).toBe('Hello, BOB!') })
