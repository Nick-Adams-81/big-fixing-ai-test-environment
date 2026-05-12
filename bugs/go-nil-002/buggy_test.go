package buggy_test

import (
	"buggy"
	"testing"
)

func TestDoubleNil(t *testing.T) {
	if got := buggy.Double(nil); got != 0 {
		t.Errorf("Double(nil) = %d, want 0", got)
	}
}

func TestDoubleValue(t *testing.T) {
	v := 5
	if got := buggy.Double(&v); got != 10 {
		t.Errorf("Double(&5) = %d, want 10", got)
	}
}

func TestDoubleZero(t *testing.T) {
	v := 0
	if got := buggy.Double(&v); got != 0 {
		t.Errorf("Double(&0) = %d, want 0", got)
	}
}

func TestDoubleNeg(t *testing.T) {
	v := -3
	if got := buggy.Double(&v); got != -6 {
		t.Errorf("Double(&-3) = %d, want -6", got)
	}
}
