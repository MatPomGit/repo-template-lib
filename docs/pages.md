# GitHub Pages biblioteki LIB

**Cel:** publiczna dokumentacja **jednego wersjonowanego komponentu wielokrotnego użytku**, jego API, instalacji i kompatybilności. Nie jest to portal badań ARC, strona końcowego produktu APP ani publiczna kopia wewnętrznego `docs/`. Status wzorca to `scaffold`, zatem przykładowa witryna nie stanowi dokumentacji działającej biblioteki.

## 1. Izolacja strony publicznej

Jedynym katalogiem źródłowym witryny jest **`pages/`** (`mkdocs.yml`: `docs_dir: pages`, `site_dir: site`). `docs/` przechowuje architekturę, ADR, strategie testowe, konfigurację wydawniczą i dokumentację operacyjną, nieprzeznaczoną domyślnie do publicznej publikacji. Nie kopiuj do Pages `profiles/`, `contracts/`, `config/`, `src/`, `examples/` bez osobnej recenzji, `AGENTS.md`, `.github/`, sekretów, logów, danych uczestników ani prywatnych rejestrów odbiorców.

Każda strona i grafika w `pages/` wymaga jawnego wpisu w `config/pages-policy.json`. Zgodnie z istniejącą polityką LIB źródłem jest Markdown lub pasywny obraz PNG/JPEG/WebP/AVIF/ICO; surowy HTML/JS/CSS/SVG z projektu nie podlega automatycznemu dopuszczeniu. W publicznej dokumentacji nie dopuszczaj niekontrolowanych skryptów CDN, telemetrycznych trackerów ani aktywnych formularzy. Budowa MkDocs jest operacją lokalną, a nie publikacją.

GitHub Pages może być publiczne nawet dla prywatnego repozytorium. Sprawdź faktyczne ustawienia, domenę, widoczność, koszty i zakres ujawnianych informacji. **Nie konfiguruj `Deploy from a branch` wskazującego `main:/docs` ani root repo.** Dopuszczalna jest dopiero świadomie zatwierdzona publikacja przejrzanego `site/`, np. izolowanym artefaktem GitHub Actions lub gałęzią zawierającą wyłącznie treści publiczne. Automatycznego deploymentu po merge nie dodawaj do szablonu.

## 2. Struktura informacji biblioteki

| Sekcja | Informacja dla odbiorcy |
| --- | --- |
| Przegląd | Problem, zakres funkcji, docelowe platformy i ograniczenia komponentu |
| Instalacja | Zweryfikowany kanał dystrybucji, przypięta wersja, wymagania runtime i integralność pakietu |
| Pierwsze użycie | Minimalny, **rzeczywiście uruchomiony** przykład i oczekiwane wyjście |
| API | Wspierane symbole, sygnatury, typy, jednostki, wyjątki, wątki/async oraz stabilność kontraktu |
| Kompatybilność | Wersje Python/Node/JVM/.NET/Unity, OS, architektura, GPU/urządzenia wyłącznie po testach |
| Wersje i migracje | Changelog, zgodne i niezgodne zmiany, deprecjacje i przewodnik aktualizacji |
| Bezpieczeństwo | Publiczne wymagania uprawnień, ograniczenia oraz odnośnik do kanału zgłaszania podatności |
| Cytowanie | Wersja biblioteki, rzeczywisty DOI (jeśli istnieje) i zatwierdzona metryka autorstwa |

Nie twórz pustych podstron: w nowym szablonie wystarczy `pages/index.md`. Dodaj kolejne sekcje do nawigacji dopiero po wdrożeniu i przetestowaniu rzeczywistego API. Treść musi być zrozumiała dla użytkownika biblioteki. **Żadnych promptów, instrukcji dla agentów AI, uwag edytorskich, placeholderów, wewnętrznych procedur i opisów „jak pomagać w repozytorium” ani `CONTRIBUTING`.** Nie podawaj planowanej funkcji jako wdrożonej.

Dokumentacja API musi odzwierciedlać jeden kanoniczny `contracts/api.json` oraz publiczne implementacje, bez tworzenia drugiej niezależnej specyfikacji. Różnice semantyczne sprawdzaj testami kontraktowymi. Dokumentacja wersji powinna wskazywać konkretne tagi i SHA, a przykłady instalacyjne powinny działać z wydanym artefaktem, nie jedynie z lokalnego katalogu.

## 3. Platformy i dystrybucja

Przygotowuj dokumentację wyłącznie dla faktycznie obsługiwanego profilu w `profiles/`. **Python:** wersje CPython, typy i ewentualne ABI oraz wheel/sdist. **npm:** wersje Node, ESM/CJS, typy TypeScript i `exports`. **Maven:** współrzędne GAV, minimalny JDK i zależności tranzytywne. **NuGet:** Target Framework Monikers i zgodność .NET. **Unity UPM:** wersja edytora, pipeline renderowania, `asmdef` i test importu czystego projektu. **OCI:** architektury obrazów, digest, minimalny runtime i zasady uruchamiania.

Jeśli biblioteka obsługuje streaming, przetwarzanie obrazu, sygnałów EEG, dźwięku czy urządzenia pomiarowe, podaj formaty, jednostki, częstotliwości, latencję, kontrakty danych i warunki walidacji tylko po zweryfikowaniu. Nie publikuj prywatnych identyfikatorów aparatury ani konfiguracji z repozytorium `devices`. Wyniki testów syntetycznych nie dowodzą poprawności na rzeczywistym sprzęcie.

Wpisy odbiorców `app-*` i `msc-*` pokazuj wyłącznie po potwierdzeniu ich publiczności oraz prawa do ujawnienia nazwy i powiązania. ARC opisuje relacje programowe, ale nie zastępuje kanonicznego repozytorium LIB. Nie kopiuj prywatnych informacji z repozytoriów konsumentów do witryny.

## 4. Ilustracje, przykłady i bezpieczeństwo

W kodzie przykładowym nie wolno ujawniać tokenów, danych użytkowników, adresów prywatnych serwerów ani nieautoryzowanych plików. Fragmenty powinny wskazywać język, wersję biblioteki, środowisko, parametry i zweryfikowany wynik. Dla grafik podawaj alt text, źródło i licencję. Wykresy wydajności wymagają jednostek, osi, sprzętu, liczby powtórzeń, rozrzutu i jawnej metodologii. Metadane EXIF/XMP/IPTC i osadzone miniatury wymagają przeglądu przed publikacją.

Stosuj czytelny responsywny układ, nawigację klawiaturą, kontrast i WCAG 2.2 AA jako cel; nazwy symboli API i polecenia instalacyjne muszą być czytelne również na telefonie. Warto opisywać ograniczenia i niezgodności bez marketingowych obietnic niezrealizowanych funkcji.

## 5. Bramka publikacyjna Pages

1. Sprawdź tożsamość komponentu, rzeczywiście wydaną wersję i zakres zatwierdzonych materiałów. W prywatnych repozytoriach skontroluj także nazwy zależności, konsumentów i adresy URL.
2. Uruchom `python scripts/validate_pages.py`, `python scripts/validate_documentation.py` i `python -m mkdocs build --strict` z przypiętym MkDocs 1.6.1.
3. Wykonaj `python scripts/validate_rendered_pages.py --strict` dla **całego** `site/`. Wynik powinien zawierać wyłącznie zatwierdzone HTML, zasoby motywu o odpowiednich SHA-256, wygenerowane pliki MkDocs i zatwierdzone obrazy; nie może ujawniać skryptów ani dokumentacji wewnętrznej.
4. Przejrzyj wizualnie każdą stronę oraz końcowy HTML, metadane multimediów, linki, dostępność, przykłady instalacji i poprawność twierdzeń. Test automatyczny nie potwierdza prawa do publikacji.
5. Uzyskaj niezależną recenzję finalnego SHA oraz **osobną decyzję właściciela** o publikacji konkretnej witryny i domeny. Sprawdź rzeczywisty serwis po deploymentcie i przygotuj rollback.

Publikacja dokumentacji nie jest tożsama z publikacją pakietu, tagu ani GitHub Release. Zasady opisuje [procedura wydawnicza](releases.md).

