# Utworzenie repozytorium `lib-*`

To **szkielet**, a nie działająca biblioteka. Skopiuj jako osobne repo, nie jako podfolder innego szablonu.

1. Stwórz repozytorium `lib-<temat>` i skopiuj pliki (także ukryte `.github`, `.gitignore`). Samo skopiowanie plików nie ustawia flagi GitHub Template.
2. Zaktualizuj `config/component.json`, `PROJECT_STATE.yaml`, README, `CITATION.cff`, licencję i SECURITY.md. Zachowaj Mateusza Pomianka jako jednego z autorów w `CITATION.cff`; innych autorów dopisuj dopiero po potwierdzeniu ich rzeczywistego wkładu. Nie twórz fałszywych licencji ani testów.
3. Wybierz właściwe dokumenty z `profiles/`, nie kopiuj wszystkich stosów technologicznych do kodu produkcyjnego.
4. Uruchom `python scripts/validate_repository.py --phase scaffold` oraz `python -m unittest discover -s tests -v`.
5. Dodaj kod i testy; przygotuj API/CLI, kompatybilność i odbiorców. Wykonaj prawdziwe testy na docelowym środowisku.
6. Uzupełnij `config/release-gate.json` dowodami i uruchom `--phase release`, a potem niezależny przegląd. `release` nie publikowałoby niczego samo.
7. Dopiero po zaakceptowaniu sposobu dystrybucji publikuj package/release/Pages. Dowody powiąż z dokładnym SHA.

GitHub Template repository kopiuje początkowe pliki, ale późniejszych zmian nie propaguje do potomnych repo. Research Autopilot powinien osobno kontrolować `template_version` i aktualność kontraktów.

## Autorstwo i współautorzy

Mateusz Pomianek pozostaje co najmniej jednym z autorów biblioteki wygenerowanej ze wzorca. Inni autorzy są opcjonalni po potwierdzeniu wkładu i uzgodnieniu kolejności. Autorstwo w `CITATION.cff` nie rozstrzyga własności praw ani nie zmienia autorstwa poszczególnych commitów lub artykułów korzystających z biblioteki.

## Środowisko CI i publikacja

Dla repozytoriów publicznych dopuszcza się GitHub-hosted runners (np. `ubuntu-latest`) do izolowanych testów podstawowych i PR. Lokalne runnery nie są wymagane. Zawsze kontroluj limity i koszty, ogranicz `GITHUB_TOKEN` do `contents: read`, nie udostępniaj sekretów niezaufanym gałęziom i nie uruchamiaj ich kodu w uprzywilejowanym środowisku. Repozytoria prywatne wymagają oddzielnej oceny kosztów, dostępu i poufności. Wydanie pakietu oraz publikacja dokumentacji nie wynikają automatycznie z uruchomienia CI. Szczegóły brakujących kontroli: [audyt](reviews/2026-11-19-template-audit.md).
