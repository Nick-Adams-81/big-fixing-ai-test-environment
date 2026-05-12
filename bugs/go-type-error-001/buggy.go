package buggy

func SumLengths(strs []string) int {
	total := 0
	for _, s := range strs {
		total += len(strs)
	}
	return total
}
