package buggy_test

import (
	"buggy"
	"testing"
)

func TestCountOccurrencesBasic(t *testing.T) {
	if got := buggy.CountOccurrences([]int{1, 2, 2, 3, 2}, 2); got != 3 {
		t.Errorf("CountOccurrences = %d, want 3", got)
	}
}

func TestCountOccurrencesNone(t *testing.T) {
	if got := buggy.CountOccurrences([]int{1, 2, 3}, 9); got != 0 {
		t.Errorf("CountOccurrences = %d, want 0", got)
	}
}

func TestCountOccurrencesAll(t *testing.T) {
	if got := buggy.CountOccurrences([]int{5, 5, 5}, 5); got != 3 {
		t.Errorf("CountOccurrences = %d, want 3", got)
	}
}

func TestCountOccurrencesEmpty(t *testing.T) {
	if got := buggy.CountOccurrences([]int{}, 1); got != 0 {
		t.Errorf("CountOccurrences = %d, want 0", got)
	}
}

func TestCountOccurrencesOne(t *testing.T) {
	if got := buggy.CountOccurrences([]int{1, 2, 3, 4}, 3); got != 1 {
		t.Errorf("CountOccurrences = %d, want 1", got)
	}
}
