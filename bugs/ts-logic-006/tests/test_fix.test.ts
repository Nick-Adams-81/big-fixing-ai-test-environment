import { expect, test } from 'vitest'
import { unique } from '../buggy'

test('removes duplicates', () => { expect(unique([1, 2, 2, 3, 3, 3])).toEqual([1, 2, 3]) })
test('no duplicates unchanged', () => { expect(unique([1, 2, 3])).toEqual([1, 2, 3]) })
test('all duplicates', () => { expect(unique([5, 5, 5])).toEqual([5]) })
test('empty array', () => { expect(unique([])).toEqual([]) })
test('strings', () => { expect(unique(['a', 'b', 'a'])).toEqual(['a', 'b']) })
