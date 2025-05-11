from playwright.sync_api import sync_playwright
import pytest

# Oczekiwana wartość maski ciasteczka cookiePolicyGDPR po akceptacji analitycznych
EXPECTED_MASK = "3"

@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_accept_analytics_cookie_mask(browser_name):
    with sync_playwright() as p:
        # Uruchamiamy wskazaną przeglądarkę w trybie headless
        browser = getattr(p, browser_name).launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Wejdź na stronę ING
        page.goto("https://www.ing.pl", timeout=60000)

        # Otwórz panel ciasteczek
        page.click("button.js-cookie-policy-main-settings-button")

        # Zaznacz opcję analitycznych
        page.click("div.js-checkbox[name='CpmAnalyticalOption']")

        # Zaakceptuj zaznaczone
        page.click("button:has-text('Zaakceptuj zaznaczone')")

        # Poczekaj krótko na zapis ciasteczek
        page.wait_for_timeout(1000)

        # Znajdź ciasteczko cookiePolicyGDPR i sprawdź jego wartość
        mask_cookie = next(c for c in context.cookies() if c["name"] == "cookiePolicyGDPR")
        assert mask_cookie["value"] == EXPECTED_MASK, (
            f"Oczekiwana maska '{EXPECTED_MASK}', ale mamy '{mask_cookie['value']}'"
        )

        # Zamknij przeglądarkę
        browser.close()