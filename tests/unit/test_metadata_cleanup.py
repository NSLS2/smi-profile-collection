import builtins

from smi_beamline.plans.metadata_cleanup import RE_MD_WHITELIST, clean_re_md


def _answers(monkeypatch, answers):
    iterator = iter(answers)
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(iterator))


def test_whitelist_matches_current_re_md_keys():
    assert RE_MD_WHITELIST == {
        "SAF_number",
        "beamline_attenuators",
        "beamline_name",
        "beamline_sample_environment",
        "cycle",
        "data_session",
        "facility",
        "project_name",
        "proposal",
        "sample_name",
        "scan_id",
        "start_datetime",
        "tiled_access_tags",
        "username",
        "versions",
    }


def test_clean_re_md_no_extras_makes_no_changes(capsys):
    md = {"scan_id": 1, "sample_name": "s"}

    assert clean_re_md(md) == []
    assert md == {"scan_id": 1, "sample_name": "s"}
    assert "no extraneous keys" in capsys.readouterr().out


def test_clean_re_md_aborts_before_per_key_prompts(monkeypatch):
    md = {"scan_id": 1, "junk": {"a": 1}}
    _answers(monkeypatch, ["n"])

    assert clean_re_md(md) == []
    assert md == {"scan_id": 1, "junk": {"a": 1}}


def test_clean_re_md_deletes_skips_and_ends(monkeypatch):
    md = {"scan_id": 1, "a_extra": 1, "b_extra": 2, "c_extra": 3}
    _answers(monkeypatch, ["y", "d", "s", "e"])

    assert clean_re_md(md) == ["a_extra"]
    assert md == {"scan_id": 1, "b_extra": 2, "c_extra": 3}
