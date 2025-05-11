import os
from playwright.sync_api import sync_playwright, TimeoutError

EXPECTED = {"cookiePolicyGDPR", "cookiePolicyGDPR__details", "cookiePolicyINCPS"}

def test_accept_analytics_cookie():
    browser_name = os.getenv("BROWSER", "chromium")
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch(headless=True)
        # wymuś polski, żeby banner był po polsku
        context = browser.new_context(locale="pl-PL")
        page = context.new_page()

        # 1) Wejdź i poczekaj na sieć
        page.goto("https://www.ing.pl")
        page.wait_for_load_state("networkidle", timeout=60000)

        # 2) Otwórz panel ciastek
        settings_btn = page.locator("button.js-cookie-policy-main-settings-button")
        settings_btn.wait_for(state="visible", timeout=90000)
        settings_btn.click(timeout=90000)

        # 3) Zaznacz analityczne
        analytics_chk = page.locator("div.js-checkbox[name='CpmAnalyticalOption']")
        analytics_chk.wait_for(state="visible", timeout=60000)
        analytics_chk.click()

        # 4) Zaakceptuj
        accept_btn = page.locator("button:has-text('Zaakceptuj zaznaczone')")
        try:
            accept_btn.wait_for(state="visible", timeout=30000)
            accept_btn.click()
        except TimeoutError:
            # fallback na angielski, gdyby nie było polskiego
            page.click("button:has-text('Accept selected')", timeout=30000)

        # 5) Poczekaj na zapis ciastek
        page.wait_for_timeout(2000)

        # 6) Sprawdź cookie
        names = {c["name"] for c in context.cookies()}
        assert EXPECTED & names, f"Brak expected ciastek, mamy tylko {names!r}"

        browser.close()