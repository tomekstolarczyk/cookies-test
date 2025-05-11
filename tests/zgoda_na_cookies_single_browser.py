from playwright.sync_api import sync_playwright

### ciasteczka, po których bedziemy weryfikować ###
EXPECTED = {"cookiePolicyGDPR", "cookiePolicyGDPR__details", "cookiePolicyINCPS"}

def test_accept_analytics_cookie_simple():

    with sync_playwright() as p:
        ### uruchamiamy wybrana przegladarke headless ###
        browser = p.chromium.launch(headless=True)
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