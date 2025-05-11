import os
from playwright.sync_api import sync_playwright

### ciasteczka, po których bedziemy weryfikować ###
EXPECTED = {"cookiePolicyGDPR", "cookiePolicyGDPR__details", "cookiePolicyINCPS"}


def test_accept_analytics_cookie():
    # Odczytujemy nazwe przegladarki z zmiennej srodowiskowej
    browser_name = os.getenv("BROWSER", "chromium")

    with sync_playwright() as p:
        # Uruchamiamy wybrana przegladarke w trybie headless
        browser = getattr(p, browser_name).launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Przechodzimy na strone ING
        page.goto("https://www.ing.pl", timeout=60000)

        # 1. Otwórz panel ciasteczek używając selektora klasy
        page.wait_for_selector("button.js-cookie-policy-main-settings-button", timeout=60000)
        page.click("button.js-cookie-policy-main-settings-button")

        # 2. Zaznacz opcję analitycznych po selektorze klasy i atrybucie name
        page.wait_for_selector(".js-checkbox[name='CpmAnalyticalOption']", timeout=60000)
        page.click(".js-checkbox[name='CpmAnalyticalOption']")

        # 3. Kliknij "Zaakceptuj zaznaczone" - tu pozostawiamy tekst bo nie ma klasy
        page.wait_for_selector("button:has-text('Zaakceptuj zaznaczone')", timeout=60000)
        page.click("button:has-text('Zaakceptuj zaznaczone')")

        # 4. Dajemy chwilę na zapis ciastek
        page.wait_for_timeout(1000)

        # 5. Pobierz ciasteczka i weryfikuj obecność
        cookies = context.cookies()
        names = {c['name'] for c in cookies}
        assert EXPECTED & names, (
            f"Nie znaleziono żadnego z expected cookies {EXPECTED!r}, mamy tylko {names!r}"
        )

        # Zamknij sesję przeglądarki
        browser.close()
