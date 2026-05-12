package buggy_test

import (
	"buggy"
	"testing"
)

func TestClampInRange(t *testing.T) {
	if got := buggy.Clamp(5, 0, 10); got != 5 {
		t.Errorf("Clamp(5,0,10) = %v, want 5", got)
	}
}

func TestClampAtLo(t *testing.T) {
	if got := buggy.Clamp(0, 0, 10); got != 0 {
		t.Errorf("Clamp(0,0,10) = %v, want 0", got)
	}
}

func TestClampAtHi(t *testing.T) {
	if got := buggy.Clamp(10, 0, 10); got != 10 {
		t.Errorf("Clamp(10,0,10) = %v, want 10", got)
	}
}

func TestClampBelowLo(t *testing.T) {
	if got := buggy.Clamp(-1, 0, 10); got != 0 {
		t.Errorf("Clamp(-1,0,10) = %v, want 0", got)
	}
}

func TestClampAboveHi(t *testing.T) {
	if got := buggy.Clamp(11, 0, 10); got != 10 {
		t.Errorf("Clamp(11,0,10) = %v, want 10", got)
	}
}
