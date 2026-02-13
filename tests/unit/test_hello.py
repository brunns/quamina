from hamcrest import assert_that, equal_to

from quamina import hello


def test_hello():
    actual = hello()

    assert_that(actual, equal_to("Hello from quamina!"))
