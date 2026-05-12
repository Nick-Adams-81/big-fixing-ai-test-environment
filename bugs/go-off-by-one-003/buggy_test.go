package buggy_test

import (
	"buggy"
	"testing"
)

func TestLastNThree(t *testing.T) {
	got := buggy.LastN([]int{1, 2, 3, 4, 5}, 3)
	if len(got) != 3 || got[0] != 3 || got[1] != 4 || got[2] != 5 {
		t.Errorf("LastN returned %v, want [3 4 5]", got)
	}
}

func TestLastNOne(t *testing.T) {
	got := buggy.LastN([]int{10, 20, 30}, 1)
	if len(got) != 1 || got[0] != 30 {
		t.Errorf("LastN returned %v, want [30]", got)
	}
}

func TestLastNTwo(t *testing.T) {
	got := buggy.LastN([]int{1, 2, 3, 4}, 2)
	if len(got) != 2 || got[0] != 3 || got[1] != 4 {
		t.Errorf("LastN returned %v, want [3 4]", got)
	}
}

func TestLastNAll(t *testing.T) {
	s := []int{1, 2, 3}
	got := buggy.LastN(s, 3)
	if len(got) != 3 {
		t.Errorf("LastN returned %v, want %v", got, s)
	}
}
