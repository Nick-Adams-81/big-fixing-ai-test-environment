export function firstN<T>(arr: T[], n: number): T[] {
    return arr.slice(0, n - 1);
}
