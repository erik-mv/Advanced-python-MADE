from time import sleep

import pytest

from realty import Realty
    

def test_can_instantiate_realty():
    Realty(name="Vasya",area=40.0)


def test_realty_can_greet_a_person():
    expected_name = "Vasya"
    vasya_realty = Realty(name="Vasya",area=40.0)
    greeting = vasya_realty.greet()
    assert expected_name in greeting, (
        f"name {expected_name} should be present in greeting. "
        f"while your greeting is: {greeting}"
    )


def test_realty_calculate_monthly_payment_correctly():
    monthly_payment = Realty.calculate_monthly_payment(value=1_000_000, years=5, interest=0.1)
    expected_monthly_payment = 21247
    assert monthly_payment == pytest.approx(expected_monthly_payment, abs=0.5), (
        f"calculated monthly payment is {monthly_payment} while it should be {expected_monthly_payment}"
    )


def test_can_load_realty_from_file():
    loaded_realty = Realty.load_from_file(filepath="vasya_realty.txt")
    expected_realty = Realty(name="Vasya", area=40.0)
    assert expected_realty == loaded_realty


def test_imitate_workload():
    sleep(10)


def test_realty_raise_exception_with_empty_area():
    with pytest.raises(ValueError):
        Realty(name="Vasya", area=None)



    