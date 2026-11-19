# Niezależny audyt szablonu `repo-template-lib`

**Data:** 2026-11-19. **Punkt odniesienia:** `main` @ `5c085bbe5a4ee6dbc1f2dccacfc5ce078b9e927b`.  
**Metoda:** statyczna inspekcja kodu walidatora, manifestów, dokumentacji, testów i konfiguracji GitHub. **Nie uruchomiono** jednostkowych ani integracyjnych testów, nie zbudowano pakietu i nie wdrożono żadnego release.  
**Zakres:** repozytorium wielokrotnego użytku `lib-*`, nie samodzielna aplikacja `app-*` ani manuskrypt badawczy `msc-*`.

## Ocena

**Ocena orientacyjna 6,5/10**, oparta na eksperckiej analizie źródeł, a nie wykonanym audycie środowiska.

| Kryterium | Ocena orientacyjna |
| --- | ---: |
| Architektura i rozdzielenie odpowiedzialności | 8/10 |
| Kontrakt API i kompatybilność | 7/10 |
| Wydania i reprodukowalność | 7/10 |
| Bezpieczeństwo i licencje (założenia) | 7/10 |
| Walidacja automatyczna | 4/10 |
| CI oraz egzekwowanie jakości | 2/10 |
| Dokumentacja profili dystrybucji | 8/10 |
| Integracja z `msc-*`, `app-*` i `arc-*` | 7/10 |

### Mocne strony

1. Rozdzielono odpowiedzialność za bibliotekę, jej kontrakt i wydania od programów ARC, samodzielnych aplikacji oraz repozytoriów manuskryptowych.
2. `contracts/api.json`, `docs/contracts.md`, `docs/compatibility.md` i `docs/consumers.md` przewidują stabilizację API, deprecjację, zgodność konsumentów i migracje.
3. W `config/release-gate.json` wszystkie dowody na start są negatywne; walidator `--phase release` wymaga deklaracji testów, instalacji, audytu zależności i zgody wydawcy.
4. Profile `python`, `npm`, `maven`, `nuget`, `unity` i `oci` są opcjonalne. Nie wymagają budowania wszystkich technologii w jednym repozytorium.
5. Dokumentacja odróżnia status `NOT_RUN`/`NOT_VERIFIED` od testów wykonanych rzeczywiście; nie nadaje domyślnie niepotwierdzonych licencji ani DOI.
6. Repozytorium ma flagę `is_template=true`; podstawowe dokumenty i testy strukturalne już istnieją.

## Ustalenia i plan naprawy

| ID | Priorytet | Potwierdzony problem / ryzyko | Rekomendacja |
| --- | --- | --- | --- |
| LIB-01 | P0 | Nie ma `.github/workflows/` ani wykonanych GitHub Actions. Ruleset `main` blokuje usunięcie i non-fast-forward, ale nie wymaga pozytywnego CI ani review. | Minimalny CI dla scaffold, testów, manifestów i kontraktów; po stabilizacji obowiązkowe status checks i recenzja. |
| LIB-02 | P0 | `scripts/validate_repository.py` parsuje `contracts/api.json` tylko jako JSON i sprawdza opcjonalne pole `schema_version` z domyślną wartością 1. Nie sprawdza poprawności publicznych symboli ani zgodności `name`, `api_version` i `config/component.json`. | Ścisły schemat danych i testy spójności wersji/identyfikatorów; fail-closed na błędnych typach, placeholderach i niespójnym API. |
| LIB-03 | P0 | Release gate akceptuje ręcznie ustawione wartości `true`, 40-znakowy SHA i 64-znakowy checksum o poprawnym formacie. Nie wiąże ich z wykonanym testem, HEAD i rzeczywistą paczką. | Automatyczne powiązanie dowodów ze zbudowanym artefaktem, jego sumą kontrolną, exact SHA i raportem z instalacji/testów. Weryfikacja niezależnej recenzji pozostaje osobną bramką. |
| LIB-04 | P0 | `LICENSE` pozostaje placeholderem nawet gdy `license_spdx` w `config/component.json` przyjmie pozornie poprawną wartość. `.gitignore` nie chroni przed wymuszonym dodaniem sekretów ani przed wcześniej śledzonymi plikami. | Kontrola zgodności rzeczywistej licencji z manifestem, skan sekretów i zawartości dystrybuowanego archiwum; rozróżnić licencje zależności, modeli i SDK. |
| LIB-05 | P1 | `PROJECT_STATE.yaml` jest tylko sprawdzany pod kątem istnienia; nie następuje parsowanie ani porównanie z `config/component.json` i `contracts/api.json`. | Walidacja schematu YAML, typu repozytorium, komponentu, wersji, właściciela i stanu release. |
| LIB-06 | P1 | `CITATION.cff` ma `REPLACE_FAMILY`/`REPLACE_GIVEN`; brak wymogu stałego autora podstawowego. | Zachować Mateusza Pomianka jako co najmniej jednego autora w każdym projekcie wygenerowanym z szablonu. Dopuszczać rzeczywistych współautorów po potwierdzeniu wkładu. |
| LIB-07 | P1 | Brak idempotentnego inicjalizatora profilu biblioteki; ręczne kopiowanie przykładów może pozostawić `REPLACE_*` i niespójne metadane. | Prosta inicjalizacja `lib-*` z wyborem jednego profilu i testem wygenerowanego repo; nie instalować nieużywanych stosów. |
| LIB-08 | P1 | `--phase release` wymaga niepustego `consumers`, mimo że niezależna, nowa biblioteka może nie mieć konsumentów; jednocześnie nie weryfikuje niepustego `public_entrypoints` i poprawności publikowanej paczki. | Nie fałszować konsumentów. Wymagać udokumentowanego scenariusza konsumpcji i testu smoke w czystym środowisku; sprawdzać rzeczywistą zawartość API/artefaktu. |
| LIB-09 | P1 | Brak rzeczywistego testu backward compatibility / breaking changes dla kolejnych wersji. Same `breaking_change_policy` i SemVer nie wykrywają regresji. | Dodać testy zgodności symboli, typów i zachowania API między wersjami oraz przewodnik migracyjny dla zmian niekompatybilnych, zależnie od ekosystemu. |
| LIB-10 | P1 | `docs/privacy.md` nakazuje podanie klasy danych i network egress w `config/component.json`, ale biblioteczny manifest nie ma tych pól. To rozjazd z odziedziczonym szablonem `app-*`. | Dopasować dokumentację do rzeczywistego kontraktu biblioteki; dodać klasyfikację tylko gdy biblioteka faktycznie przetwarza dane lub komunikuje się z siecią. |
| LIB-11 | P1 | Nie istnieje test budowy wheel/sdist, npm package, UPM package, AAR, nupkg ani obrazu OCI. Profile są dokumentacją, nie gotowymi wydaniami. | Zaimplementować *jeden wybrany* profil end-to-end (build, clean install, import/API smoke test), bez wymogu obsługi wszystkich platform. |
| LIB-12 | P2 | `template_version` 1.0.0 jest zaszyte w kodzie walidatora; obecny regex SemVer weryfikuje ogólny kształt, nie pełną semantykę. Nie ma testów migracji potomnych repozytoriów. | Wersjonować szablon i kontrakty niezależnie od wersji paczki, dodawać testy migracyjne i walidację standardu SemVer. |

Dodatkowo `contracts/api.json` z pustą listą `public_entrypoints` jest poprawny jako **scaffold**, nie stanowi jednak dowodu istnienia API gotowego do wydania. Wykryte luki oznaczają brak pokrycia walidacyjnego, a nie potwierdzone błędy produkcyjne.

## Zasady obowiązujące przy wykorzystaniu szablonu

**Autorstwo.** Mateusz Pomianek pozostaje co najmniej jednym z autorów w `CITATION.cff` i metadanych biblioteki. Można dopisać dodatkowych, faktycznych współautorów po ustaleniu i potwierdzeniu ich wkładu oraz kolejności. Nie zakłada się, że autor repozytorium jest autorem każdego commita, że posiada wszystkie prawa osób trzecich ani że automatycznie jest współautorem dowolnego artykułu wykorzystującego tę bibliotekę.

**Runnery GitHub.** Dla repozytoriów **publicznych** dopuszczalne są GitHub-hosted runners do odizolowanych, bezpiecznych testów CI (`pull_request`/`push`), np. `ubuntu-latest`. Nie narzuca się lokalnych runnerów do podstawowego testowania. Dla repo prywatnych należy ustalić koszty, poufność i dostępność. Minimalne `permissions: contents: read`; nie ujawniać sekretów niezaufanym PR, nie wykonywać kodu z forków przez uprzywilejowane `pull_request_target` ani na stałych zaufanych runnerach. Publikacja pakietu i Pages pozostaje osobną decyzją, a dodatkowe wydatki wymagają zgody.

**Granice repozytorium.** `lib-*` posiada własny kod i publiczne API. `app-*` i `msc-*` konsumują wersjonowany pakiet po tagu/SHA/digest; `arc-*` kataloguje badania. Nie duplikować kodu ani globalnego schedulera. Przypiętych SHA użytych w zamrożonych eksperymentach nie aktualizować automatycznie.

## Backlog i definicja ukończenia

### P0 — kontrola warunkująca uznanie wzorca za operacyjny
- [ ] Podstawowe CI oraz skuteczne wymagane kontrole PR po stabilizacji.
- [ ] Walidacja API i spójności `contracts/api.json` z manifestem oraz testy negatywne.
- [ ] Bramka wydania weryfikująca zbudowany artefakt, checksum, exact SHA, raporty i rzeczywisty tekst licencji.
- [ ] Skan sekretów / łańcucha dostaw zgodnie z przyjętą polityką.

### P1 — jakość gotowej biblioteki
- [ ] Walidacja YAML, stanu i metadanych wszystkich źródeł.
- [ ] Inicjalizator z obowiązkowym autorem Mateuszem Pomiankiem i opcjonalnymi współautorami.
- [ ] Działający pakiet i clean-install smoke test **jednego** wybranego profilu.
- [ ] Test kompatybilności API, przykładowego odbiorcy i dokumentacja deprecjacji.
- [ ] Korekta dokumentacji prywatności odpowiednio do rodzaju biblioteki.

### P2 — utrzymywalność
- [ ] SemVer, changelog, zgodność wsteczna szablonu i test migracji.

## Scenariusz akceptacyjny

Z `Use this template` utworzyć `lib-example`, zachować w metadanych Mateusza Pomianka, opcjonalnie dopisać rzeczywistego współautora, wybrać **jeden** profil (np. Python), wygenerować pakiet z minimalnym publicznym API i kontraktem, wykonać clean install oraz smoke test odbiorcy. Na GitHub-hosted runner publicznego repozytorium uruchomić CI, następnie sprawdzić, że błędne API, wersja, licencja, brak testu lub checksum zablokują release. Przed publikacją wykonać wymagane review. Nie potrzeba danych uczestników ani urządzeń, jeśli profil tego nie wymaga.

**Zakres niniejszego PR:** zapis audytu i rekomendacji, korekta autorstwa w szablonie, dopuszczenie GitHub-hosted runners i aktualizacja powiązanych dokumentów. **Nie wykonuje:** CI, testów pakietów, skanerów, aktualizacji rulesetów, publikacji ani wdrożenia całego backlogu. Checkboxy celowo pozostają otwarte.
