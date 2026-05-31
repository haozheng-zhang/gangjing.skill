import pytest

from gangjing.roles import ROLES, get_role, list_roles


def test_all_required_modes_load():
    expected = {"default", "product", "tech", "startup", "github", "academic", "gentle"}
    assert expected.issubset(ROLES)
    assert {role.name for role in list_roles()}.issuperset(expected)


def test_invalid_mode_has_clear_error():
    with pytest.raises(ValueError, match="Unknown gangjing mode"):
        get_role("rainbow")
