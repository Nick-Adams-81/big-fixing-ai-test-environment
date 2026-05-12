package buggy_test

import (
	"buggy"
	"testing"
)

func TestFib0(t *testing.T) {
	if got := buggy.Fibonacci(0); got != 0 { t.Errorf("Fibonacci(0) = %d, want 0", got) }
}

func TestFib1(t *testing.T) {
	if got := buggy.Fibonacci(1); got != 1 { t.Errorf("Fibonacci(1) = %d, want 1", got) }
}

func TestFib2(t *testing.T) {
	if got := buggy.Fibonacci(2); got != 1 { t.Errorf("Fibonacci(2) = %d, want 1", got) }
}

func TestFib5(t *testing.T) {
	if got := buggy.Fibonacci(5); got != 5 { t.Errorf("Fibonacci(5) = %d, want 5", got) }
}

func TestFib7(t *testing.T) {
	if got := buggy.Fibonacci(7); got != 13 { t.Errorf("Fibonacci(7) = %d, want 13", got) }
}
