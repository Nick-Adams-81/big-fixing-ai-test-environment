package buggy

func Repeat(s string, n int) string {
	result := ""
	for i := 0; i < n-1; i++ {
		result += s
	}
	return result
}
