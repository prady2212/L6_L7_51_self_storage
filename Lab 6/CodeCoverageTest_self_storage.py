import pytest
from self_storage import rent_due, access_allowed, payment_status


# --- Tests for rent_due ---
def test_rent_due_invalid_size():
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("extra_large", 5, False, False)

def test_rent_due_negative_months():
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -2, False, False)

def test_rent_due_covered_months():
    assert rent_due("small", 1, False, False) == 0

def test_rent_due_standard_non_climate():
    assert rent_due("small", 4, False, False) == 240

def test_rent_due_climate_with_discount():
    assert rent_due("medium", 10, True, True) == 735


# --- Tests for access_allowed ---
def test_access_owner():
    assert access_allowed(10, 3, True) is True

def test_access_after_hours():
    assert access_allowed(23, 1, False) is False

def test_access_regular_hours():
    assert access_allowed(14, 2, False) is True


# --- Tests for payment_status ---
def test_payment_current():
    assert payment_status(5, True, False) == "current"

def test_payment_grace():
    assert payment_status(2, False, True) == "grace"

def test_payment_lien():
    assert payment_status(-20, False, False) == "lien"