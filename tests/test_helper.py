import os
import tempfile
import pytest
from Helper.helper import check_file_exists, make_dirs, already_downloaded
from unittest.mock import patch


# ── Test 1: check_file_exists ─────────────────────────────────────

def test_check_file_exists_returns_message_when_exists():
    tmp = tempfile.mkdtemp()
    result = check_file_exists(tmp)
    assert result is not None
    assert 'exists' in result.lower()


def test_check_file_exists_returns_none_when_missing():
    result = check_file_exists('/nonexistent/path/xyz')
    assert result is None

# ── Test 2: make_dirs ─────────────────────────────────────────────

def test_make_dirs_creates_directory():
    tmp = tempfile.mkdtemp()
    new_folder = os.path.join(tmp, 'new_folder')
    assert not os.path.exists(new_folder)  # doesn't exist yet
    make_dirs(new_folder)
    assert os.path.isdir(new_folder)       # now it does


def test_make_dirs_does_not_raise_if_already_exists():
    tmp = tempfile.mkdtemp()
    make_dirs(tmp)  # folder already exists
    make_dirs(tmp)  # calling again should not raise any error


# ── Test 3: already_downloaded ────────────────────────────────────

def test_already_downloaded_returns_false_for_fake_year():
    result = already_downloaded(9999)
    assert result is False


def test_already_downloaded_returns_true_when_folder_exists():
    with patch('Helper.helper.os.path.isfile', return_value=True):
        result = already_downloaded(2024)
        assert result is True


def test_already_downloaded_returns_false_when_folder_empty():
    with patch('Helper.helper.os.path.isfile', return_value=False):
        result = already_downloaded(2024)
        assert result is False