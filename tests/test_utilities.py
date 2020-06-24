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


def test_can_check_env_is_set(monkeypatch):
    assert utilities.no_nonesP(["test", "test2"]) is True
    assert utilities.no_nonesP(["test", None]) is False
