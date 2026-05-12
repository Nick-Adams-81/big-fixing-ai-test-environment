package buggy

func LastN(s []int, n int) []int {
	return s[len(s)-n-1:]
}
