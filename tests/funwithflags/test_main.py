import re
import runpy


def test_app_should_print_a_uuid(capsys):
    # when: same as `python -m funwithflags`
    runpy.run_module("funwithflags", run_name="__main__")

    # then
    actual = capsys.readouterr().out
    assert re.fullmatch(r"[a-f0-9]{32}\n", actual)
