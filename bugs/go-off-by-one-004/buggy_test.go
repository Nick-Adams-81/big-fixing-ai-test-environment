package buggy_test

import (
	"buggy"
	"testing"
)

func TestContainsLast(t *testing.T) {
	if !buggy.Contains([]int{1, 2, 3, 4, 5}, 5) {
		t.Error("Contains should find last element 5")
	}
}

func TestContainsFirst(t *testing.T) {
	if !buggy.Contains([]int{1, 2, 3}, 1) {
		t.Error("Contains should find first element 1")
	}
}

func TestContainsMid(t *testing.T) {
	if !buggy.Contains([]int{10, 20, 30}, 20) {
		t.Error("Contains should find middle element 20")
	}
}

func TestContainsMissing(t *testing.T) {
	if buggy.Contains([]int{1, 2, 3}, 9) {
		t.Error("Contains should not find 9")
	}
}

func TestContainsEmpty(t *testing.T) {
	if buggy.Contains([]int{}, 1) {
		t.Error("Contains should return false for empty slice")
	}
}
