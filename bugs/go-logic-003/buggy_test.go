package buggy_test

import (
	"buggy"
	"testing"
)

func TestAbsPositive(t *testing.T) {
	if got := buggy.Abs(5); got != 5 {
		t.Errorf("Abs(5) = %d, want 5", got)
	}
}

func TestAbsNegative(t *testing.T) {
	if got := buggy.Abs(-3); got != 3 {
		t.Errorf("Abs(-3) = %d, want 3", got)
	}
}

func TestAbsZero(t *testing.T) {
	if got := buggy.Abs(0); got != 0 {
		t.Errorf("Abs(0) = %d, want 0", got)
	}
}

func TestAbsNegTen(t *testing.T) {
	if got := buggy.Abs(-10); got != 10 {
		t.Errorf("Abs(-10) = %d, want 10", got)
	}
}
