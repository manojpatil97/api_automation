import pytest
from playwright.sync_api import Playwright

API_KEY = "free_user_3HMvVBIJYv2CHIJ72kwWa3cJ411"

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):

    request_context = playwright.request.new_context(
        extra_http_headers={
            "x-api-key": API_KEY
        }
    )

    yield request_context

    request_context.dispose()
 