export function countTruthy(arr: unknown[]): number {
    return arr.filter(x => !x).length;
}
