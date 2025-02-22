#!/usr/bin/env python3

import re

from garak import __version__, cli

ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def test_version_command(capsys):
    cli.main(["--version"])
    result = capsys.readouterr()
    output = ansi_escape.sub("", result.out)
    assert "garak" in output
    assert f"v{__version__}" in output
    assert len(output.strip().split("\n")) == 1


def test_probe_list(capsys):
    cli.main(["--list_probes"])
    result = capsys.readouterr()
    output = ansi_escape.sub("", result.out)
    for line in output.strip().split("\n"):
        assert re.match(
            r"^probes: [a-z0-9_]+.[A-Za-z0-9_]+( 🌟)?$", line
        ) or line.startswith("garak LLM probe v")


def test_detector_list(capsys):
    cli.main(["--list_detectors"])
    result = capsys.readouterr()
    output = ansi_escape.sub("", result.out)
    for line in output.strip().split("\n"):
        assert re.match(
            r"^detectors: [a-z0-9_]+.[A-Za-z0-9_]+( 🌟)?$", line
        ) or line.startswith("garak LLM probe v")


def test_generator_list(capsys):
    cli.main(["--list_generators"])
    result = capsys.readouterr()
    output = ansi_escape.sub("", result.out)
    for line in output.strip().split("\n"):
        assert re.match(
            r"^generators: [a-z0-9_]+.[A-Za-z0-9_]+( 🌟)?$", line
        ) or line.startswith("garak LLM probe v")


def test_run_all_probes(capsys):
    cli.main(["-m", "test", "-p", "all", "-d", "always.Pass"])
    result = capsys.readouterr()
    last_line = result.out.strip().split("\n")[-1]
    assert re.match("^✔️  garak done: complete in [0-9]+\\.[0-9]+s$", last_line)
