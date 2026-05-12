package buggy_test

import (
	"buggy"
	"testing"
)

func TestIsEven2(t *testing.T) {
	if !buggy.IsEven(2) { t.Error("2 should be even") }
}

func TestIsEven3(t *testing.T) {
	if buggy.IsEven(3) { t.Error("3 should not be even") }
}

func TestIsEven0(t *testing.T) {
	if !buggy.IsEven(0) { t.Error("0 should be even") }
}

func TestIsEven7(t *testing.T) {
	if buggy.IsEven(7) { t.Error("7 should not be even") }
}

func TestIsEven100(t *testing.T) {
	if !buggy.IsEven(100) { t.Error("100 should be even") }
}
