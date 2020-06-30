import pytest

from mabd import utilities

def test_get_env_var_can_get_arbitrary_env_var(monkeypatch):
    monkeypatch.setenv("KEY", "nonsense")
    value = utilities.get_env_var("KEY")
    assert value == "nonsense"

    monkeypatch.setenv("KEY", "bleh")
    value = utilities.get_env_var("KEY")
    assert value == "bleh"

    monkeypatch.delenv("KEY")
    assert utilities.get_env_var("KEY") == None


def test_get_env_var_checked_exits_if_check_fails(monkeypatch):
    nokey = "AN_UNTHINKABLE_KEY"
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        utilities.get_env_var_checked(nokey)
    assert pytest_wrapped_e.type == SystemExit
