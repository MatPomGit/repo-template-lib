# Procedura autonomicznej pracy agentów LIB

Podstawą jest [AGENTS.md](../AGENTS.md). Dokument nie nadaje uprawnień do produkcji, danych prywatnych, licencji lub publikacji.

## 1. DoR i rozpoznanie

Odczytaj stan `main` i SHA, Issues, PR/drafty, lease, `config/component.json`, `contracts/api.json`, `PROJECT_STATE.yaml` i wybrany profil `profiles/*/AGENTS.md`. Ustal aktualnych konsumentów, istniejące regresje, ryzyko R0–R3 i granice uprawnień. Kontynuuj rozpoczęte zadanie zamiast tworzyć duplikat.

## 2. Implementacja

Pracuj na małych, testowanych zmianach, bez kopiowania kodu do `msc-*` i `app-*`. Zmiana API/ABI wymaga aktualizacji kontraktu, SemVer, kompatybilności, migracji i testów odbiorców. Nie fabrykuj weryfikacji sprzętu. Testy niezaufanego kodu realizuj poza stałymi runnerami i sekretami. Dla operacji o skutkach zewnętrznych wymagaj odrębnej zgody, planu wycofania i idempotentnego przebiegu.

## 3. Walidacja i niezależna recenzja

Uruchom `python scripts/validate_repository.py --phase scaffold`, `python scripts/validate_documentation.py`, `python scripts/validate_pages.py`, `python -m unittest discover -s tests -v`. Dla konkretnego pakietu wykonaj również build, clean install, kontrolę licencji/zależności przechodnich, test API i kompatybilności na aktualnym SHA. Raportuj `PASS/FAIL/NOT_RUN/UNAVAILABLE/SKIPPED` bez przypisywania testom wyników, których nie uzyskano.

Niezależny recenzent bada finalny diff i dowody; własna ocena nie jest niezależną recenzją. `COMMENTED/ACCEPT` nie zastępuje formalnego `APPROVED`.

## 4. Integracja, release i Pages

Merge, utworzenie artefaktu, publikacja do registry, instalacja u odbiorcy oraz strona GitHub Pages to różne etapy. `config/release-gate.json` opisuje deklaracje, nie poświadcza niezależnie wykonania testów. Przed release sprawdź licencję, artefakt i hash, supply-chain, odbiorców i upoważnienie właściciela.

Publiczna witryna korzysta tylko z allowlisty `pages/`, nigdy z `docs/`, `.github/` i instrukcji agentowych. Sprawdź wygenerowany HTML, zasoby, widoczność i prawa do treści, szczególnie w prywatnym repozytorium. Nie publikuj automatycznie na merge.

## 5. DoD, blokady i sprzątanie

Zakończ dopiero po potwierdzonych kryteriach, testach na finalnym SHA, właściwej recenzji i integracji. Zapisz stan, ograniczenia i punkt wznowienia w istniejącym Issue. Nie usuwaj nieznanych gałęzi, worktree lub procesów i nie przerywaj cudzych obliczeń.
