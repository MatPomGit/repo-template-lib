# Wydania i dystrybucja

Wydanie wymaga jawnej wersji, sprawdzenia kontraktów, licencji, izolowanej instalacji, testów regresji i manifestu artefaktów.
Dołącz checksums SHA-256, kompatybilność, odpowiednie pliki SPDX i plan cofnięcia zmian.
`--phase release` sprawdza **deklarowane dowody** i lokalną obecność raportu oraz artefaktu. Pole `release_artifact_path` w `config/release-gate.json` ma wskazywać istniejący plik w obrębie repozytorium; jego SHA-256 musi zgadzać się z `release_artifact_sha256`. Walidator odrzuca placeholder licencji oraz wybrane niezgodności między SPDX a tekstem `LICENSE`, lecz nie prowadzi pełnego audytu prawnego.\n\nWalidacja nie potwierdza pochodzenia raportu, powiązania `tested_commit_sha` z rzeczywistym CI/HEAD, jakości testów ani praw do zależności. Potrzebna jest niezależna kontrola przed publikacją.

Registry: npm/Maven/NuGet/GHCR w GitHub Packages; Python wheel przez GitHub Releases lub osobno zatwierdzony indeks; Unity UPM przez wersjonowany Git URL. APK, EXE i instalatory przez Releases.
Nie uruchamiaj publikacji automatycznie, jeśli naruszyłoby to ograniczenie zero-spend.
