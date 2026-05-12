export function lastN<T>(arr: T[], n: number): T[] {
    return arr.slice(arr.length - n - 1);
}
