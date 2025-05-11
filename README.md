# Automatyczny test zgody na cookies dla ING.pl

---

## Opis projektu

Ten projekt zawiera zestaw testów automatyzujących akceptację ciasteczek analitycznych na stronie **[https://www.ing.pl](https://www.ing.pl)** z wykorzystaniem **Playwright** i **pytest**. Testy są powtarzalne dzięki uruchamianiu każdej sesji w czystym kontekście przeglądarki.

Dostępne skrypty:

* `zgoda_na_cookies_single_browser.py` – test uruchamiany lokalnie dla jednej przeglądarki (domyślnie Chromium).
* `zgoda_na_cookies_multi_browser.py` – test uruchamiający sprawdzenie w trzech przeglądarkach jednocześnie (Chromium, Firefox, WebKit) z wykorzystaniem `@pytest.mark.parametrize`.
* `zgoda_na_cookies_for_automation.py` – test dedykowany pod CI/CD (odczyt zmiennej środowiskowej `BROWSER`).
* `.github/workflows/ci.yml` – GitHub Actions workflow, który ma uruchamiać `zgoda_na_cookies_for_automation.py` w macierzy przeglądarek na Windows.

---

## Wymagania wstępne

* **Python 3.10+**
* `pip` (menedżer pakietów)
* System operacyjny: Linux, macOS lub Windows
* Dostęp do internetu (do pobrania przeglądarek i otwarcia strony ING)

---

## Instalacja i konfiguracja

1. **Skopiuj repozytorium**

   ```bash
   git clone https://github.com/<TwojUser>/<Repo>.git
   cd <Repo>
   ```

2. **Utwórz i aktywuj wirtualne środowisko**

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   .\.venv\Scripts\activate     # Windows PowerShell
   ```

3. **Zainstaluj zależności**

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   # lub ręcznie:
   pip install pytest playwright
   python -m playwright install
   ```

---

## Uruchamianie testów lokalnie

### Single-browser (Chromium domyślnie)

```bash
pytest -q zgoda_na_cookies_single_browser.py
```

### Multi-browser (Chromium, Firefox, WebKit)

```bash
pytest -q zgoda_na_cookies_multi_browser.py
```

### Test pod CI/CD (zmienna BROWSER)

* Domyślnie przeglądarka to Chromium:

  ```bash
  pytest -q zgoda_na_cookies_for_automation.py
  ```
* Aby wymusić inną przeglądarkę:

  ```bash
  export BROWSER=firefox     # Linux/macOS
  set BROWSER=firefox        # Windows PowerShell
  pytest -q zgoda_na_cookies_for_automation.py
  ```

---

## GitHub Actions (CI)

Workflow `.github/workflows/ci.yml` powinien uruchomić test `zgoda_na_cookies_for_automation.py` w macierzy przeglądarek na Windows.

**Schemat działania:**

1. Checkout repozytorium
2. Setup Python 3.12
3. Instalacja zależności (`pytest`, `playwright`)
4. Pobranie binarek przeglądarek: `playwright install`
5. Uruchomienie testu dla `BROWSER=${{ matrix.browser }}`

> **Uwaga:** Lokalne testy przechodzą, ale w CI pojawił się problem z odpaleniem testu. Obecnie workflow nie przechodzi – prawdopodobnie dotyczy to ścieżki do pliku lub konfiguracji zmiennej środowiskowej.

---

## Troubleshooting

* Sprawdź, czy plik `tests/zgoda_na_cookies_for_automation.py` istnieje i jest w poprawnej lokalizacji.
* Zweryfikuj, czy w workflow podajesz ścieżkę: `pytest -q tests/zgoda_na_cookies_for_automation.py`.
* Upewnij się, że `BROWSER` jest przekazywany w `env:` kroku.
* Przetestuj uruchamianie testu w PowerShell (środowisko podobne do CI).

---

## Kontakt

W razie pytań proszę o kontakt przed spotkaniem rekrutacyjnym.
