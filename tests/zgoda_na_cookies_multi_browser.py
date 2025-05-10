"""
Ten sam test co poprzednio, ale uruchomiony trzykrotnie dla:
- chromium
- firefox
- webkit
"""

import pytest
from playwright.sync_api import sync_playwright

### ciasteczka, po których bedziemy weryfikować ###
EXPECTED = {"cookiePolicyGDPR", "cookiePolicyGDPR__details", "cookiePolicyINCPS"}

@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_accept_analytics_cookie_multi(browser_name):


    with sync_playwright() as p:
        ### uruchamiamy wybrana przegladarke headless ###
        browser = getattr(p, browser_name).launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        ### wchodzimy na ing ###
        page.goto("https://www.ing.pl", timeout=60000)

        ### otwieramy panel cookies ###
        page.click("button.js-cookie-policy-main-settings-button")

        ### Akceptujemy analityczne ###
        page.click("div.js-checkbox[name='CpmAnalyticalOption']")

        ### Akceptujemy zaznaczone ###
        page.click("button:has-text('Zaakceptuj zaznaczone')")

        ### Asercja: co najmniej jedno z oczekiwanych ciastek jest w zestawie ###
        names = {c["name"] for c in context.cookies()}
        assert EXPECTED & names, f"Brak oczekiwanego cookie w: {names}"

        ### zamykamy sesje ###
        browser.close()