import { expect, test } from 'vitest'
import { firstN } from '../buggy'

test('returns first 3 elements', () => {
    expect(firstN([1, 2, 3, 4, 5], 3)).toEqual([1, 2, 3])
})

test('returns first 1 element', () => {
    expect(firstN([10, 20, 30], 1)).toEqual([10])
})

test('returns all elements', () => {
    expect(firstN([1, 2, 3], 3)).toEqual([1, 2, 3])
})

test('returns first 2', () => {
    expect(firstN([0, 1, 2, 3, 4], 2)).toEqual([0, 1])
})

test('returns empty for n=0', () => {
    expect(firstN([1, 2, 3], 0)).toEqual([])
})
