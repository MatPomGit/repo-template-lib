# Utworzenie repozytorium `lib-*`

To **szkielet**, a nie działająca biblioteka. Skopiuj jako osobne repo, nie jako podfolder innego szablonu.

1. Stwórz repozytorium `lib-<temat>` i skopiuj pliki (także ukryte `.github`, `.gitignore`). Samo skopiowanie plików nie ustawia flagi GitHub Template.
2. Zaktualizuj `config/component.json`, `PROJECT_STATE.yaml`, README, `CITATION.cff`, licencję i SECURITY.md. Zachowaj Mateusza Pomianka jako jednego z autorów w `CITATION.cff`; innych autorów dopisuj dopiero po potwierdzeniu ich rzeczywistego wkładu. Nie twórz fałszywych licencji ani testów.
3. Wybierz właściwe dokumenty z `profiles/`, nie kopiuj wszystkich stosów technologicznych do kodu produkcyjnego.
4. Uruchom `python scripts/validate_repository.py --phase scaffold`, `python scripts/validate_documentation.py`, `python scripts/validate_pages.py` i `python -m unittest discover -s tests -v`. Przed publikacją Pages wykonaj także `python -m mkdocs build --strict` (MkDocs 1.6.1) i `python scripts/validate_rendered_pages.py`; zbudowane `site/` nie jest automatycznie wdrażane.
5. Dodaj kod i testy; przygotuj API/CLI, kompatybilność, odbiorców oraz rzeczywiste [komponenty](docs/architecture/components.md), [model zagrożeń](docs/security/threat-model.md) i [ADR](docs/adr/README.md). Stosuj [limity](docs/documentation.md). Wykonaj prawdziwe testy na docelowym środowisku.
6. Uzupełnij `config/release-gate.json` dowodami i uruchom `--phase release`, a potem niezależny przegląd. `release` nie publikowałoby niczego samo.
7. GitHub Pages ma osobny katalog `pages/`, allowlistę `config/pages-policy.json` i osobny przegląd. Nie publikuj `docs/` ani instrukcji agentowych, sprawdź widoczność witryny przy prywatnym repo. Dopiero po zaakceptowaniu sposobu dystrybucji publikuj package/release/Pages. Nie twórz `CONTRIBUTING.md`; dowody powiąż z dokładnym SHA.

GitHub Template repository kopiuje początkowe pliki, ale późniejszych zmian nie propaguje do potomnych repo. Research Autopilot powinien osobno kontrolować `template_version` i aktualność kontraktów.

## Autorstwo i współautorzy

Mateusz Pomianek pozostaje co najmniej jednym z autorów biblioteki wygenerowanej ze wzorca. Inni autorzy są opcjonalni po potwierdzeniu wkładu i uzgodnieniu kolejności. Autorstwo w `CITATION.cff` nie rozstrzyga własności praw ani nie zmienia autorstwa poszczególnych commitów lub artykułów korzystających z biblioteki.

## Środowisko CI i publikacja

Dla repozytoriów publicznych dopuszcza się GitHub-hosted runners (np. `ubuntu-latest`) do izolowanych testów podstawowych i PR. Lokalne runnery nie są wymagane. Zawsze kontroluj limity i koszty, ogranicz `GITHUB_TOKEN` do `contents: read`, nie udostępniaj sekretów niezaufanym gałęziom i nie uruchamiaj ich kodu w uprzywilejowanym środowisku. W prywatnych repozytoriach powstałych ze wzorca job `validate` jest domyślnie pomijany, aby nie uruchamiać płatnego GitHub-hosted runnera bez zgody; świadome uruchomienie CI wymaga osobnej konfiguracji i kontroli kosztów, dostępu i poufności. Wydanie pakietu oraz publikacja dokumentacji nie wynikają automatycznie z uruchomienia CI. Szczegóły brakujących kontroli: [audyt](reviews/2026-11-19-template-audit.md).

## Standard E4.0: publiczne API i wersjonowane wydania

Przygotuj stronę wyłącznie z zatwierdzonego `pages/` zgodnie z [polityką Pages](docs/pages.md). Opisuj tylko zaimplementowane i przetestowane symbole API, przykłady instalacji i kompatybilność. Kontroluj zasoby źródłowe i końcowy `site/`, a przy repo prywatnym rzeczywistą widoczność Pages. Wykonaj `python scripts/validate_rendered_pages.py --strict` po `mkdocs build --strict`.

Wydanie biblioteki wymaga [bramek R0–R4](docs/releases.md), wersji SemVer niezależnej od `template_version`, zamrożonego kontraktu, clean install z faktycznego pakietu i sprawdzenia odbiorców. Dla profili Python/npm/Maven/NuGet/Unity UPM/OCI stosuj tylko odpowiadający rzeczywistemu wdrożeniu kanał. Oddziel GitHub Release, registry i Pages. Nie dopisuj fikcyjnych atestacji ani raportów. Brak egzekwowanego CI/review pozostawia `HOLD`; bez dodatkowych kosztów i automatycznego deploymentu.
