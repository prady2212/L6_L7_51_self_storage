import pytest
from self_storage import rent_due, access_allowed, payment_status


# --- Branch Tests: rent_due ---
def test_rent_due_invalid_unit():
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("giant", 2, False, False)

def test_rent_due_invalid_months():
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -1, False, False)

def test_rent_due_member_large_unit():
    # Tests branch: is_member is True, but unit_size == "large"
    assert rent_due("large", 3, False, True) == 0

def test_rent_due_member_non_large():
    # Tests branch: is_member is True and unit_size != "large"
    assert rent_due("small", 2, False, True) == 0

def test_rent_due_extra_le_zero():
    # Tests extra <= 0 branch
    assert rent_due("medium", 1, False, False) == 0

def test_rent_due_non_climate_extra_under_6():
    # rate = 80, extra <= 6
    assert rent_due("small", 3, False, False) == 160

def test_rent_due_climate_extra_under_6():
    # rate = 120, extra <= 6
    assert rent_due("small", 3, True, False) == 240

def test_rent_due_non_climate_extra_over_6():
    # extra = 7 (>6), rate = 80 - 10 = 70
    assert rent_due("small", 8, False, False) == 490

def test_rent_due_climate_extra_over_6():
    # extra = 7 (>6), rate = 120 - 10 - 5 = 105
    assert rent_due("small", 8, True, False) == 735


# --- Branch Tests: access_allowed ---
def test_access_owner_valid():
    assert access_allowed(12, 4, True) is True

def test_access_owner_excess_visitors():
    assert access_allowed(12, 5, True) is False

def test_access_early_hours():
    # hour < 6 is True
    assert access_allowed(5, 1, False) is False

def test_access_late_hours():
    # hour < 6 is False, hour > 22 is True
    assert access_allowed(23, 1, False) is False

def test_access_non_owner_allowed():
    # hour valid, visitors <= 2
    assert access_allowed(12, 2, False) is True

def test_access_non_owner_denied_visitors():
    # hour valid, visitors > 2
    assert access_allowed(12, 3, False) is False


# --- Branch Tests: payment_status ---
def test_payment_autopay_no_prior_late_current():
    assert payment_status(0, True, False) == "current"

def test_payment_non_autopay_prior_late_current():
    assert payment_status(15, False, True) == "current"

def test_payment_grace_period():
    assert payment_status(-10, False, False) == "grace"

def test_payment_lien_status():
    assert payment_status(-11, False, False) == "lien"