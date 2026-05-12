package buggy_test

import (
	"buggy"
	"testing"
)

func TestFirstNThree(t *testing.T) {
	got := buggy.FirstN([]int{1, 2, 3, 4, 5}, 3)
	want := []int{1, 2, 3}
	if len(got) != len(want) {
		t.Errorf("FirstN returned %v, want %v", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Errorf("FirstN[%d] = %d, want %d", i, got[i], want[i])
		}
	}
}

func TestFirstNOne(t *testing.T) {
	got := buggy.FirstN([]int{10, 20, 30}, 1)
	if len(got) != 1 || got[0] != 10 {
		t.Errorf("FirstN returned %v, want [10]", got)
	}
}

func TestFirstNTwo(t *testing.T) {
	got := buggy.FirstN([]int{0, 1, 2, 3}, 2)
	if len(got) != 2 || got[0] != 0 || got[1] != 1 {
		t.Errorf("FirstN returned %v, want [0 1]", got)
	}
}

func TestFirstNAll(t *testing.T) {
	s := []int{1, 2, 3}
	got := buggy.FirstN(s, 3)
	if len(got) != 3 {
		t.Errorf("FirstN returned %v, want %v", got, s)
	}
}
