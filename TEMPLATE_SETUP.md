# Utworzenie repozytorium `lib-*`

To **szkielet**, nie działająca aplikacja ani biblioteka. Skopiuj jako osobne repo, nie jako podfolder innego szablonu.

1. Stwórz repozytorium `lib-<temat>` i skopiuj pliki (także ukryte `.github`, `.gitignore`). Samo skopiowanie plików nie ustawia flagi GitHub Template.
2. Zaktualizuj `config/component.json`, `PROJECT_STATE.yaml`, README, `CITATION.cff`, licencję i SECURITY.md. Nie twórz fałszywych licencji ani testów.
3. Wybierz właściwe dokumenty z `profiles/`, nie kopiuj wszystkich stosów technologicznych do kodu produkcyjnego.
4. Uruchom `python scripts/validate_repository.py --phase scaffold` oraz `python -m unittest discover -s tests -v`.
5. Dodaj kod i testy; przygotuj API/CLI, kompatybilność i odbiorców. Wykonaj prawdziwe testy na docelowym środowisku.
6. Uzupełnij `config/release-gate.json` dowodami i uruchom `--phase release`, a potem niezależny przegląd. `release` nie publikowałoby niczego samo.
7. Dopiero po zaakceptowaniu sposobu dystrybucji publikuj package/release/Pages. Dowody powiąż z dokładnym SHA.

GitHub 8Template repository kopiuje początkowe pliki, ale późniejszych zmian nie propaguje do potomnych repo. Research Autopilot powinien osobno kontrolować `template_version` i aktualność kontraktów.
