package buggy

func CountOccurrences(s []int, target int) int {
	count := 0
	for _, v := range s {
		if v != target {
			count++
		}
	}
	return count
}
