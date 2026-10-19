from pathlib import Path

from amazonvision.config import RunMode, Settings, data_base_dir


def test_simulated_and_real_modes_use_separate_data_dirs():
    simulated = Settings(_env_file=None)
    real = Settings(_env_file=None, mode=RunMode.REAL)
    assert simulated.data_root == data_base_dir() / "simulado"
    assert real.data_root == data_base_dir() / "real"
    assert simulated.db_path != real.db_path


def test_explicit_data_dir_wins(tmp_path: Path):
    settings = Settings(_env_file=None, mode=RunMode.REAL, data_dir=tmp_path)
    assert settings.db_path == tmp_path / "db" / "amazonvision.sqlite"


def test_environment_variables_are_read(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("AV_MODE", "real")
    monkeypatch.setenv("AV_DATA_DIR", str(tmp_path))
    settings = Settings(_env_file=None)
    assert settings.mode is RunMode.REAL
    assert settings.data_root == tmp_path


def test_defaults_bind_to_localhost_only():
    settings = Settings(_env_file=None)
    assert settings.host == "127.0.0.1"
    assert "0.0.0.0" not in settings.allowed_hosts  # noqa: S104
