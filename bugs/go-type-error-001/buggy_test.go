package buggy_test

import (
	"buggy"
	"testing"
)

func TestSumLengthsBasic(t *testing.T) {
	if got := buggy.SumLengths([]string{"hello", "world"}); got != 10 {
		t.Errorf("SumLengths = %d, want 10", got)
	}
}

func TestSumLengthsSingle(t *testing.T) {
	if got := buggy.SumLengths([]string{"abc"}); got != 3 {
		t.Errorf("SumLengths = %d, want 3", got)
	}
}

func TestSumLengthsEmpty(t *testing.T) {
	if got := buggy.SumLengths([]string{}); got != 0 {
		t.Errorf("SumLengths = %d, want 0", got)
	}
}

func TestSumLengthsMixed(t *testing.T) {
	if got := buggy.SumLengths([]string{"a", "bb", "ccc"}); got != 6 {
		t.Errorf("SumLengths = %d, want 6", got)
	}
}
