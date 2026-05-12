import { expect, test } from 'vitest'
import { sumUpTo } from '../buggy'

test('sum 1..5 = 15', () => {
    expect(sumUpTo(5)).toBe(15)
})

test('sum 1..1 = 1', () => {
    expect(sumUpTo(1)).toBe(1)
})

test('sum 1..10 = 55', () => {
    expect(sumUpTo(10)).toBe(55)
})

test('sum 1..0 = 0', () => {
    expect(sumUpTo(0)).toBe(0)
})

test('sum 1..3 = 6', () => {
    expect(sumUpTo(3)).toBe(6)
})
