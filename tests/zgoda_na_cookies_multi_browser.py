"""
Test sprawdza, czy po zaakceptowaniu ciasteczek analitycznych
w przeglądarce zapisuje się ciasteczko 'cookiePolicyGDPR' o wartości '3', 
po kolei dla 3 przeglądarek chromium, firefox oraz webkit.
"""

### na poczatek importujemy sync_playwright z biblioteki Playwright ###
from playwright.sync_api import sync_playwright

### będziemy sprawdzać czy ciasteczko cookiePolicyGDPR po zapisaniu ma wartość 3 ###
EXPECTED_MASK = "3"

### Pytest uruchomi test trzy razy po kolei dla różnych przeglądarek ###
import pytest
@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])

def test_accept_analytics_cookie_mask(browser_name):
    with sync_playwright() as p:

        ### uruchamiamy odpowiednią przeglądarke w trybie headless ###
        browser = getattr(p, browser_name).launch(headless=True)

        ### tworzymy nowy, czysty kontekst – izolowana sesja, nowe ciasteczka ###
        ### dzięki temu test jest powtarzalny i nie wpływa na stan innych testów ###
        context = browser.new_context()

        ### otwieramy nową strone w ramach tego kontekstu ###
        page = context.new_page()

        ### wchodzimy na stronę ing ###
        page.goto("https://www.ing.pl", timeout=60000)

        ### w panel wyboru ciasteczek klikamy dostosuj ###
        ### selektor CSS: element <button> z klasą js-cookie-policy-main-settings-button ###
        page.click("button.js-cookie-policy-main-settings-button")

        ### zaznaczamy opcję wyboru ciastek analitycznych ###
        ### selektor CSS: <div> z klasą js-checkbox i atrybutem name='CpmAnalyticalOption' ###
        page.click("div.js-checkbox[name='CpmAnalyticalOption']")

        ### akceptujemy zaznaczone ###
        ### pseudo-selektor Playwright: klik w <button> zawierający dany tekst ###
        page.click("button:has-text('Zaakceptuj zaznaczone')")

        ### poczekajmy chwile na zapis ciasteczek ###
        page.wait_for_timeout(1000)

        ### znajdujemy ciasteczko cookiePolicyGDPR ###
        mask_cookie = next(c for c in context.cookies() if c["name"] == "cookiePolicyGDPR")
        
        ### Weryfikujemy, że ciasteczko istnieje i ma oczekiwaną wartość ###
        assert mask_cookie is not None, "Nie znaleziono ciasteczka cookiePolicyGDPR"
        assert mask_cookie["value"] == EXPECTED_MASK, (
            f"Oczekiwana maska '{EXPECTED_MASK}', ale mamy '{mask_cookie['value']}'"
        )

        ### zamykamy przeglądarkę ###
        browser.close()
