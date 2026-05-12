import re
from pathlib import Path

_LANGUAGE_LABELS = {
    "python": ("Python", "python"),
    "typescript": ("TypeScript", "typescript"),
    "go": ("Go", "go"),
}


def system_prompt(language: str) -> str:
    lang_name, _ = _LANGUAGE_LABELS.get(language, ("", ""))
    return (
        f"You are an expert software engineer specializing in debugging {lang_name} code.\n"
        f"You will be given a buggy {lang_name} file and its failing test suite.\n"
        "Your task is to identify the bug and return a unified diff patch that fixes it.\n\n"
        "Rules:\n"
        "- Output ONLY the unified diff patch, nothing else — no explanation, no prose.\n"
        "- Use exactly this header format:\n"
        "  --- a/<filename>\n"
        "  +++ b/<filename>"
    )


def build_prompt(buggy_code: str, tests: str, entrypoint: str, language: str) -> str:
    _, lang_tag = _LANGUAGE_LABELS.get(language, ("", ""))
    return (
        f"### {entrypoint}\n```{lang_tag}\n{buggy_code}\n```\n\n"
        f"### tests\n```{lang_tag}\n{tests}\n```\n\n"
        f"Produce a unified diff patch to fix the bug in {entrypoint}."
    )


def extract_patch(text: str, entrypoint: str) -> str:
    text = text.strip()
    if text.startswith("---"):
        return text + "\n"
    if m := re.search(r"```(?:diff|patch)?\n(.*?)```", text, re.DOTALL):
        return m.group(1).strip() + "\n"
    escaped = re.escape(entrypoint)
    if m := re.search(rf"(--- a/{escaped}.*)", text, re.DOTALL):
        return m.group(1).strip() + "\n"
    return ""


def read_tests(bug_dir: Path, language: str) -> str:
    if language == "go":
        test_files = sorted(bug_dir.glob("*_test.go"))
    else:
        test_files = sorted((bug_dir / "tests").glob("test_fix*"))
    return "\n\n".join(f.read_text() for f in test_files)
