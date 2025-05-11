import os
from playwright.sync_api import sync_playwright

### ciasteczka, po których bedziemy weryfikować ###
EXPECTED = {"cookiePolicyGDPR", "cookiePolicyGDPR__details", "cookiePolicyINCPS"}


def test_accept_analytics_cookie():
    ### odczytujemy browser z env ###
    browser_name = os.getenv("BROWSER", "chromium")

    with sync_playwright() as p:
        ### uruchamiamy wybraną przeglądarkę headless ###
        browser = getattr(p, browser_name).launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        ### wchodzimy na ing ###
        page.goto("https://www.ing.pl", timeout=60000)

        ### otwieramy panel cookies ###
        page.wait_for_selector("button:has-text('Dostosuj')", timeout=60000)
        page.click("button:has-text('Dostosuj')")

        ### Akceptujemy analityczne ###
        page.wait_for_selector("div.js-checkbox[name='CpmAnalyticalOption']", timeout=60000)
        page.click("div.js-checkbox[name='CpmAnalyticalOption']")

        ### Akceptujemy zaznaczone ###
        page.wait_for_selector("button:has-text('Zaakceptuj zaznaczone')", timeout=60000)
        page.click("button:has-text('Zaakceptuj zaznaczone')")

        ###  Dajemy chwilę, żeby baner zanikał i cookies się zapisały ### 
        page.wait_for_timeout(1000)

        ### Pobieramy cookies ###
        cookies = context.cookies()
        names = {c["name"] for c in cookies}

        ### Asercja: co najmniej jedno z oczekiwanych ciastek jest w zestawie ###
        assert EXPECTED & names, (
            f"Nie znaleziono żadnego z expected cookies {EXPECTED!r}, "
            f"a mamy tylko {names!r}"
        )

        ### zamykamy sesje ###
        browser.close()
