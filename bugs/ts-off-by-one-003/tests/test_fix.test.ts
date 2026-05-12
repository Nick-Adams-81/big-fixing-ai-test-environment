import { expect, test } from 'vitest'
import { lastN } from '../buggy'

test('last 3 of 5', () => {
    expect(lastN([1, 2, 3, 4, 5], 3)).toEqual([3, 4, 5])
})

test('last 1', () => {
    expect(lastN([10, 20, 30], 1)).toEqual([30])
})

test('last 2', () => {
    expect(lastN([1, 2, 3, 4], 2)).toEqual([3, 4])
})

test('all elements', () => {
    expect(lastN([1, 2, 3], 3)).toEqual([1, 2, 3])
})
