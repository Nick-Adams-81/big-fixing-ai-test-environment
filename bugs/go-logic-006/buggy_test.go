package buggy_test

import (
	"buggy"
	"testing"
)

func TestMaxALarger(t *testing.T) {
	if got := buggy.Max(10, 3); got != 10 { t.Errorf("Max(10,3) = %d, want 10", got) }
}

func TestMaxBLarger(t *testing.T) {
	if got := buggy.Max(2, 7); got != 7 { t.Errorf("Max(2,7) = %d, want 7", got) }
}

func TestMaxEqual(t *testing.T) {
	if got := buggy.Max(5, 5); got != 5 { t.Errorf("Max(5,5) = %d, want 5", got) }
}

func TestMaxNeg(t *testing.T) {
	if got := buggy.Max(-1, -5); got != -1 { t.Errorf("Max(-1,-5) = %d, want -1", got) }
}
