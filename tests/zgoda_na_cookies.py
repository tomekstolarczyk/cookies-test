from playwright.sync_api import sync_playwright

# Wybierz ciasteczko, po którym wolisz weryfikować obecność
EXPECTED = {"cookiePolicyGDPR", "cookiePolicyGDPR__details", "cookiePolicyINCPS"}

def test_accept_analytics_cookie_simple():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.ing.pl", timeout=60000)

        ### otwieramy panel cookies
        page.click("button.js-cookie-policy-main-settings-button")

        ### Zaznaczamy analityczne
        page.click("div.js-checkbox[name='CpmAnalyticalOption']")

        ### Zaakceptuj zaznaczone
        page.click("button:has-text('Zaakceptuj zaznaczone')")

        ###. Pobierz cookies
        cookies = context.cookies()
        names = {c["name"] for c in cookies}

        ###. Asercja: co najmniej jedno z oczekiwanych ciastek jest w zestawie
        assert EXPECTED & names, (
            f"Nie znaleziono żadnego z expected cookies {EXPECTED!r}, "
            f"a mamy tylko {names!r}"
        )

        browser.close()