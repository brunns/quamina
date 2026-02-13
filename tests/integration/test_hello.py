import httpx
from brunns.matchers.response import is_response
from hamcrest import assert_that
from mbtest.imposters import Imposter, Predicate, Response, Stub
from mbtest.matchers import had_request

from quamina import hello


def test_request_to_mock_server(mock_server):
    message = hello()

    imposter = Imposter(Stub(Predicate(path="/test"), Response(body=message)), port=4545)

    with mock_server(imposter):
        test_url = imposter.url / "test"
        response = httpx.get(f"{test_url}")

        assert_that(response, is_response().with_status_code(200).and_body(message))
        assert_that(imposter, had_request().with_path("/test").and_method("GET"))
