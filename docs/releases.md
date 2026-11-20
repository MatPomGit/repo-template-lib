# Wersjonowanie, testowanie i wydania bibliotek LIB

**Zakres:** biblioteki `lib-*` z autonomicznym cyklem życia, publicznym kontraktem API, testami i przemyślanym sposobem dystrybucji. Szablon ma status `scaffold`. Deklaracja `release_candidate` lub pozytywny walidator nie dowodzą powstania używalnego pakietu.

## 1. Wersje i kontrakt kompatybilności

Kanoniczna wersja biblioteki to `config/component.json:version`, zgodna z SemVer 2.0.0. `template_version` i `PROJECT_STATE.yaml:template_version` oznaczają **wersję szablonu**, nie wersję wydanego API. Manifest ekosystemu (`pyproject.toml`, `package.json`, `pom.xml`, `.csproj`, `package.json` Unity) oraz tag `vX.Y.Z` muszą być spójne z wersją komponentu.

| Zmiana | Wersja |
| --- | --- |
| Niekompatybilna zmiana publicznego API, schematu, jednostek lub gwarantowanych zachowań | `MAJOR` |
| Nowa zgodna funkcja lub publiczny symbol, bez złamania istniejących konsumentów | `MINOR` |
| Poprawka zachowująca kontrakt, dokumentację i kompatybilność | `PATCH` |
| Etap prerelease/rc | `X.Y.Z-rc.N`, z jednoznaczną informacją o niestabilności |

Przy `0.x` kompatybilność może być mniej stabilna, ale **każdą** niezgodną zmianę należy jawnie opisać i przeprowadzić testy migracji konsumentów. Aktualizuj `contracts/api.json` i `CHANGELOG.md`; nie ogłaszaj stabilności niezaimplementowanych funkcji. Deprecjacja wymaga komunikatu, planu usunięcia i okresu wspierania adekwatnego do rzeczywistych odbiorców.

## 2. Macierz artefaktów i kanałów

| Profil | Artefakt | Kanał i obowiązkowy test |
| --- | --- | --- |
| Python | `wheel` oraz w razie potrzeby `sdist` | GitHub Release lub osobno autoryzowany indeks; clean install w nowym venv, import i smoke test, tag Python ABI |
| npm | Archiwum pakietu | Rejestr npm lub GitHub Packages, `npm pack`/install, `exports`, ESM/CJS i typy |
| Maven | `jar` + POM + metadane | Repozytorium Maven/GitHub Packages, clean dependency resolution, JDK i API |
| NuGet | `nupkg` (i dozwolone symbol packages) | NuGet/GitHub Packages, projekt-konsument z docelowym TFM |
| Unity UPM | Wersjonowany pakiet UPM, ewentualnie dozwolone archiwa | Git URL/tag albo zatwierdzony registry; import w czystym projekcie, `asmdef`, Unity/URP/HDRP |
| OCI | Obraz OCI i manifest wieloarchitekturowy | Zatwierdzony registry; digest, test startu, skan zależności i minimalne uprawnienia |

Nie próbuj wydawać instalatorów APK/EXE jako biblioteki: należą do odpowiednich `app-*`. Nie publikuj pakietów równolegle we wszystkich rejestrach, jeśli projekt nie obsługuje ich realnie. **GitHub Release, publikacja w package registry i GitHub Pages są trzema niezależnymi zdarzeniami**, wymagającymi osobnej autoryzacji i dowodów.

## 3. Wymagania przedwydawnicze (R0–R4)

1. **R0 – identyfikacja:** ustaw `component_id`, autora i właściciela, rzeczywistą licencję SPDX i tekst `LICENSE`, `distribution_kind`, `package_identifier` oraz kanał dostępu. Brak otwartej licencji nie oznacza automatycznej zgody na dystrybucję.
2. **R1 – kontrakty:** zamroź API z `contracts/api.json`, wersję, typy, semantykę błędów, jednostki, zachowania asynchroniczne, wymagania pamięci i współbieżność. Weryfikuj breaking changes testami i zgodnością z poprzednią stabilną wersją.
3. **R2 – jakość:** na exact SHA uruchom statyczne CI, unit/contract/integration tests, testy z rzeczywistymi konsumentami i **czystą instalację z zbudowanego pakietu**. Dla rozwiązań sprzętowych rozdziel testy syntetyczne, symulacje i rzeczywiste pomiary. Sprawdź lockfile, wersje runtime, OS i architekturę. Nie wpisuj `PASS` bez dowodu.
4. **R3 – supply chain:** wykonaj audyt licencji i zależności, sprawdź zakres pakietu, brak tokenów i metadanych prywatnych, SBOM (np. SPDX/CycloneDX), pochodzenie pakietu, sumy SHA-256 i test instalacji pobranego artefaktu. Atestację zweryfikuj niezależnie, porównując workflow, repo, exact SHA i digest. Sam wpis `approved: true` nie jest atestacją.
5. **R4 – autoryzacja:** niezależna recenzja finalnego SHA, obowiązkowe CI rzeczywiście egzekwowane w rulesecie `main` i świadoma zgoda właściciela na wersję, kanał oraz widoczność. Brak egzekwowanego review/CI oznacza `GATE_UNENFORCED / HOLD`.

W prywatnych repozytoriach podstawowy workflow może być `SKIPPED` z powodu ochrony kosztów; taki stan **nie jest PASS**. Przed wydaniem wymaga osobnego, autoryzowanego testu w środowisku izolowanym. Nigdy nie wykonuj niezaufanych PR na stałym HomeServerze/Andromedzie ani nie inicjuj płatnych runnerów bez zgody.

## 4. Manifest dowodowy i `--phase release`

`config/release-gate.json` jest rejestrem **deklarowanego** stanu: `tests_executed`, `test_report_path`, `tested_commit_sha`, `license_reviewed`, `dependency_audit_passed`, `clean_install_verified`, `public_api_verified`, `compatibility_documented`, `consumer_contracts_verified`, `publisher_approved`, `release_artifact_path` oraz `release_artifact_sha256`. Każda prawdziwa wartość wymaga odrębnego dowodu.

`python scripts/validate_repository.py --phase release` sprawdza zgodność metadanych, istnienie artefaktu i zadeklarowany digest. **Nie weryfikuje samodzielnie** oryginalnego pochodzenia raportu, powiązania `tested_commit_sha` z rzeczywistym workflow, autentyczności atestacji ani praw do zależności. Nie wolno traktować wyniku `PASS` jako zgody na publikację. Zapisz identyfikator zaufanego przebiegu CI, komendy testów, wersję środowiska, SHA źródła, digest artefaktu, identyfikator SBOM, wynik skanu i decyzję recenzenta. Tajne pliki i pełne logi badań nie powinny trafiać do publicznego wydania.

Manifest i paczka artefaktów muszą opisywać **dokładnie ten sam commit**. Nie buduj na ruchomym HEAD po sprawdzeniu innego SHA. Dla każdego pliku dystrybucyjnego wygeneruj SHA-256 i przeglądnij zawartość archiwum; przeprowadź ponowną instalację z *opublikowanego* artefaktu.

## 5. Procedura wydania i odtwarzania

Przygotuj `CHANGELOG.md`, informacje o migracji, listę wspieranych platform i `CITATION.cff` (jeśli projekt wymaga cytowania). Wykonaj izolowane testy, build, check pakietu oraz zatwierdzenie. Utwórz **niezmienny** tag `vX.Y.Z` na exact SHA, podpisz lub atestuj pakiet przez zaufany proces, a następnie opublikuj właściwy artefakt w wybranym kanale. Do GitHub Release dołącz datę, opis zmian, kompatybilność, licencję, sumy kontrolne, SBOM/provenance (jeśli faktycznie wygenerowano) i instrukcję migracji. Na koniec sprawdź pobrane pliki i ich instalację.

Przy regresji **nie przesuwaj opublikowanego tagu**. Wycofaj/demarkuj konkretny pakiet zgodnie z zasadami registry, opublikuj nowy patch lub wersję korygującą i wskaż konsumentom kompatybilne wersje. Jeśli naruszono prywatność albo supply chain, uruchom [procedurę incydentową](security/incident-response.md), uwzględniając kopie pobrane przez użytkowników. Cofnięcie Pages nie usuwa wydanego pakietu i odwrotnie.

**Stan szablonu:** `NOT_RELEASED` i `NOT_RUN` dla rzeczywistych pakietów. Testy kontraktu szkieletu nie potwierdzają gotowości wydania.

