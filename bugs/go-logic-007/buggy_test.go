package buggy_test

import (
	"buggy"
	"testing"
)

func TestFactorial0(t *testing.T) {
	if got := buggy.Factorial(0); got != 1 { t.Errorf("Factorial(0) = %d, want 1", got) }
}

func TestFactorial1(t *testing.T) {
	if got := buggy.Factorial(1); got != 1 { t.Errorf("Factorial(1) = %d, want 1", got) }
}

func TestFactorial3(t *testing.T) {
	if got := buggy.Factorial(3); got != 6 { t.Errorf("Factorial(3) = %d, want 6", got) }
}

func TestFactorial5(t *testing.T) {
	if got := buggy.Factorial(5); got != 120 { t.Errorf("Factorial(5) = %d, want 120", got) }
}

func TestFactorial4(t *testing.T) {
	if got := buggy.Factorial(4); got != 24 { t.Errorf("Factorial(4) = %d, want 24", got) }
}
