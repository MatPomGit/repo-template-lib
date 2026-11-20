# Polityka publicznego GitHub Pages

**Jedynym źródłem publicznej witryny jest osobne `pages/`, nigdy `docs/`.** `mkdocs.yml` musi mieć `docs_dir: pages` i `site_dir: site`. Każdy publiczny plik lub grafika wymaga jawnego wpisu w `config/pages-policy.json`. Źródła ograniczono do Markdown i pasywnych formatów obrazów (PNG, JPEG, WebP, AVIF, ICO). HTML, JavaScript, SVG i CSS z repozytorium nie są zatwierdzalnymi źródłami; w Markdown zabroniono aktywnych znaczników, URI skryptowych oraz obrazów pobieranych z zewnętrznych serwerów. Źródła sprawdza `python scripts/validate_pages.py`, a zbudowany wynik kontrolują `python -m mkdocs build --strict` (MkDocs 1.6.1) i `python scripts/validate_rendered_pages.py`.

Na stronie nie wolno umieszczać promptów ani poleceń do agentów AI, uwag redakcyjnych i edytorskich, placeholderów, komentarzy do autora, opisów utrzymania repozytorium lub zachęt do `CONTRIBUTING`. Tekst powinien być przeznaczony dla niezaangażowanych odbiorców i prezentować wyłącznie zatwierdzone informacje.

**Prywatność repozytorium nie oznacza prywatności GitHub Pages.** Przed publikacją zweryfikuj faktyczne ustawienia strony, widoczność, domenę, uprawnienia, prawa do materiałów, wygenerowany HTML, obrazy i ich metadane. Jeśli wymagana prywatność nie jest zapewniona, nie publikuj.

Zabroniony jest `Deploy from a branch` wskazujący `main:/docs` lub root repo. MkDocs sam w sobie nie blokuje tego błędu. Publikować można dopiero osobno autoryzowany wynik `site/` lub dedykowaną gałąź zawierającą wyłącznie zatwierdzone materiały. Sam merge nie uruchamia Pages.

Testy statyczne i analiza wygenerowanego HTML nie zastępują audytu motywu, ustawień hostingu ani niezależnego przeglądu strony i zgody właściciela. Poprawnie dodane strony muszą wymagać zmiany allowlisty i nawigacji, a nie testów regresyjnych.
