# 🚀 Automatyczny test zgody na cookies dla ING.pl

---

## 📋 Opis projektu

Ten projekt zawiera zestaw testów automatyzujących akceptację ciasteczek analitycznych na stronie **[https://www.ing.pl](https://www.ing.pl)** z wykorzystaniem **Playwright** i **pytest**. Testy są powtarzalne dzięki uruchamianiu każdej sesji w czystym kontekście przeglądarki.

**Dostępne skrypty:**

* `zgoda_na_cookies_single_browser.py` – test uruchamiany lokalnie dla jednej przeglądarki (domyślnie Chromium).
* `zgoda_na_cookies_multi_browser.py` – test uruchamiany lokalnie kolejno dla trzech przeglądarek (Chromium, Firefox, WebKit) z wykorzystaniem `@pytest.mark.parametrize`.
* `zgoda_na_cookies_for_automation.py` – test dedykowany pod CI/CD (odczyt zmiennej środowiskowej `BROWSER`).
* `.github/workflows/ci.yml` – GitHub Actions workflow, który ma uruchamiać `zgoda_na_cookies_for_automation.py` w macierzy przeglądarek na Windows.

---

## 🌳 Struktura projektu

```text
cookies-test/
├── .github/
│   └── workflows/ci.yml
├── tests/
│   ├── zgoda_na_cookies_single_browser.py
│   ├── zgoda_na_cookies_multi_browser.py
│   └── zgoda_na_cookies_for_automation.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Wymagania wstępne

* **Python 3.12**
* `pip` (menedżer pakietów)
* System operacyjny: Linux, macOS lub Windows
* Dostęp do internetu (do pobrania przeglądarek i otwarcia strony ING)

**Uwaga:** w `requirements.txt` znajduje się także `greenlet>=3.0.3`, ponieważ Playwright opiera się na tej bibliotece.

---

## ⚙️ Instalacja i konfiguracja

1. **Sklonuj repozytorium**

   ```bash
   git clone https://github.com/tomekstolarczyk/cookies-test.git
   cd cookies-test
   ```
2. **Utwórz i aktywuj wirtualne środowisko (bash)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Zainstaluj zależności**

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Pobierz binarki przeglądarek dla Playwright**

   ```bash
   python -m playwright install
   ```

---

## ▶️ Uruchamianie testów lokalnie

### 🖥️ Single-browser (Chromium domyślnie)

```bash
pytest -q tests/zgoda_na_cookies_single_browser.py
```

### 🌐 Multi-browser (Chromium, Firefox, WebKit)

```bash
pytest -q tests/zgoda_na_cookies_multi_browser.py
```

### 🔧 Test pod CI/CD (zmienna BROWSER)

* Domyślnie przeglądarka to Chromium:

  ```bash
  pytest -q tests/zgoda_na_cookies_for_automation.py
  ```
* Aby wymusić inną przeglądarkę (bash):

  ```bash
  export BROWSER=firefox
  pytest -q tests/zgoda_na_cookies_for_automation.py
  ```

---

## 🤖 Bonus: Automatyzacja w GitHub Actions CI

Workflow: `.github/workflows/ci.yml`

**Schemat działania:**

1. Checkout repozytorium
2. Setup Python 3.12
3. Instalacja zależności (`pytest`, `playwright`)
4. Pobranie binarek przeglądarek: `playwright install`
5. Uruchomienie testu dla `BROWSER=${{ matrix.browser }}`

> **WAŻNA UWAGA:** Lokalnie wszystkie testy działają, ale w GitHub Actions testy nie przechodzą przy uruchamianiu. Pracuję nad rozwiązaniem tego problemu.

---

## 📬 Kontakt

W razie pytań proszę o kontakt: **[tomasz.d.stolarczyk@gmail.com](mailto:tomasz.d.stolarczyk@gmail.com)**
