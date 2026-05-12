import subprocess
from pathlib import Path

DOCKER_IMAGE = "bug-fixer-sandbox:latest"
DEFAULT_TIMEOUT = 30

_PYTEST_CMD = [
    "python", "-m", "pytest", "/bug/tests", "-q", "--tb=no", "--no-header",
    "-p", "no:cacheprovider",
]
_VITEST_CMD = [
    "sh", "-c",
    "cd /runner && node node_modules/.bin/vitest run --root /bug --reporter verbose",
]
_GO_CMD = [
    "sh", "-c",
    "cd /bug && go test -v ./...",
]


def _ensure_image() -> None:
    result = subprocess.run(
        ["docker", "image", "inspect", DOCKER_IMAGE],
        capture_output=True,
    )
    if result.returncode != 0:
        dockerfile = Path(__file__).parent.parent / "docker" / "Dockerfile"
        subprocess.run(
            ["docker", "build", "-t", DOCKER_IMAGE, "-f", str(dockerfile),
             str(dockerfile.parent)],
            check=True,
        )


def run_tests(bug_dir: Path, language: str = "python", timeout: int = DEFAULT_TIMEOUT) -> tuple[str, str, int]:
    """Run tests for bug_dir inside a Docker sandbox. Returns (stdout, stderr, returncode)."""
    _ensure_image()
    if language == "typescript":
        cmd = _VITEST_CMD
    elif language == "go":
        cmd = _GO_CMD
    else:
        cmd = _PYTEST_CMD
    try:
        proc = subprocess.run(
            [
                "docker", "run", "--rm",
                "--network", "none",
                "--memory", "256m",
                "--cpus", "1",
                "-v", f"{bug_dir.resolve()}:/bug:ro",
                DOCKER_IMAGE,
            ] + cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        return "", f"Timed out after {timeout}s", 1
