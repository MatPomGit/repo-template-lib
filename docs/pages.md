# Polityka publicznego GitHub Pages

**Jedynym źródłem publicznej witryny jest osobne `pages/`, nigdy `docs/`.** `mkdocs.yml` musi mieć `docs_dir: pages` i `site_dir: site`. Każdy publiczny plik, grafika lub skrypt wymaga jawnego wpisu w `config/pages-policy.json`. Zmianę weryfikuje `python scripts/validate_pages.py`.

Na stronie nie wolno umieszczać promptów ani poleceń do agentów AI, uwag redakcyjnych i edytorskich, placeholderów, komentarzy do autora, opisów utrzymania repozytorium lub zachęt do `CONTRIBUTING`. Tekst powinien być przeznaczony dla niezaangażowanych odbiorców i prezentować wyłącznie zatwierdzone informacje.

**Prywatność repozytorium nie oznacza prywatności GitHub Pages.** Przed publikacją zweryfikuj faktyczne ustawienia strony, widoczność, domenę, uprawnienia, prawa do materiałów, wygenerowany HTML, obrazy i ich metadane. Jeśli wymagana prywatność nie jest zapewniona, nie publikuj.

Zabroniony jest `Deploy from a branch` wskazujący `main:/docs` lub root repo. MkDocs sam w sobie nie blokuje tego błędu. Publikować można dopiero osobno autoryzowany wynik `site/` lub dedykowaną gałąź zawierającą wyłącznie zatwierdzone materiały. Sam merge nie uruchamia Pages.

Automatyczny skan ma ograniczoną skuteczność; niezależny przegląd renderowanej strony i zgoda właściciela są nadal wymagane.
