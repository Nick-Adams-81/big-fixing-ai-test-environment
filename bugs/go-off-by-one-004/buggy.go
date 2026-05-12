package buggy

func Contains(s []int, target int) bool {
	for i := 0; i < len(s)-1; i++ {
		if s[i] == target {
			return true
		}
	}
	return false
}
