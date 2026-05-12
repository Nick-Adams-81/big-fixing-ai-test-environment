package buggy_test

import (
	"buggy"
	"testing"
)

func TestDivide10by2(t *testing.T) {
	if got := buggy.Divide(10, 2); got != 5 { t.Errorf("Divide(10,2) = %v, want 5", got) }
}

func TestDivide9by3(t *testing.T) {
	if got := buggy.Divide(9, 3); got != 3 { t.Errorf("Divide(9,3) = %v, want 3", got) }
}

func TestDivide7by1(t *testing.T) {
	if got := buggy.Divide(7, 1); got != 7 { t.Errorf("Divide(7,1) = %v, want 7", got) }
}

func TestDivide1by4(t *testing.T) {
	if got := buggy.Divide(1, 4); got != 0.25 { t.Errorf("Divide(1,4) = %v, want 0.25", got) }
}

func TestDivide0by5(t *testing.T) {
	if got := buggy.Divide(0, 5); got != 0 { t.Errorf("Divide(0,5) = %v, want 0", got) }
}
