package buggy_test

import (
	"buggy"
	"testing"
)

func TestHeadNonEmpty(t *testing.T) {
	if got := buggy.Head([]string{"a", "b", "c"}); got != "a" {
		t.Errorf("Head = %q, want %q", got, "a")
	}
}

func TestHeadEmpty(t *testing.T) {
	if got := buggy.Head([]string{}); got != "" {
		t.Errorf("Head(empty) = %q, want empty string", got)
	}
}

func TestHeadSingle(t *testing.T) {
	if got := buggy.Head([]string{"only"}); got != "only" {
		t.Errorf("Head = %q, want %q", got, "only")
	}
}
