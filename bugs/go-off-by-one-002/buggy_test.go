package buggy_test

import (
	"buggy"
	"testing"
)

func TestRepeatThree(t *testing.T) {
	got := buggy.Repeat("ab", 3)
	if got != "ababab" {
		t.Errorf("Repeat(ab,3) = %q, want %q", got, "ababab")
	}
}

func TestRepeatOnce(t *testing.T) {
	got := buggy.Repeat("hi", 1)
	if got != "hi" {
		t.Errorf("Repeat(hi,1) = %q, want %q", got, "hi")
	}
}

func TestRepeatZero(t *testing.T) {
	got := buggy.Repeat("x", 0)
	if got != "" {
		t.Errorf("Repeat(x,0) = %q, want empty", got)
	}
}

func TestRepeatFive(t *testing.T) {
	got := buggy.Repeat("a", 5)
	if got != "aaaaa" {
		t.Errorf("Repeat(a,5) = %q, want %q", got, "aaaaa")
	}
}
