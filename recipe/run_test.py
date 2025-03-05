import sys
from subprocess import call

FAIL_UNDER = "80"
COV = ["coverage"]
RUN = ["run", "--source=sanic_ext", "--branch", "-m"]
PYTEST = ["pytest", "-vv", "--color=yes", "--tb=long"]
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


if __name__ == "__main__":
    sys.exit(
        # run the tests
        call([*COV, *RUN, *PYTEST, *K])
        # maybe run coverage
        or call([*COV, *REPORT])
    )
