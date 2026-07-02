import sys
import os
from subprocess import call
from pathlib import Path

FAIL_UNDER = "80"
COV = ["coverage"]
RUN = ["run", "--source=sanic_ext", "--branch", "-m"]
PYTEST = ["pytest", "-vv", "--color=yes", "--tb=long", "-n", os.environ["CPU_COUNT"]]
REPORT = ["report", "--show-missing", "--skip-covered", f"--fail-under={FAIL_UNDER}"]

SKIPS = [
    "custom_specification",
    "default_context",
    "default_templates",
    "templating_dir",
]

#: added in https://github.com/conda-forge/tox-feedstock/pull/185
SKIPS += ["load_dependency_many_extra"]

SKIP_OR = " or ".join(SKIPS)
K = ["-k", f"not ({SKIP_OR})"]
PPT = Path("src/pyproject.toml")

if __name__ == "__main__":
    PPT.write_text(
        f"""{PPT.read_text(encoding="utf-8")}

        [tool.coverage.run]
        patch = ["subprocess"]
        """,
        encoding="utf-8"
    )
    sys.exit(
        # run the tests
        call([*COV, *RUN, *PYTEST, *K], cwd="src")
        # maybe run coverage
        or call([*COV, *REPORT], cwd="src")
    )
