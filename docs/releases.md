# Wydania i dystrybucja

Wydanie wymaga jawnej wersji, sprawdzenia kontraktów, licencji, izolowanej instalacji, testów regresji i manifestu artefaktów.
Dołącz checksums SHA-256, kompatybilność, odpowiednie pliki SPDX i plan cofnięcia zmian.
`--phase release` sprawdza **deklarowane dowody**, nie samodzielną walidację jakości.

Registry: npm/Maven/NuGet/GHCR w GitHub Packages; Python wheel przez GitHub Releases lub osobno zatwierdzony indeks; Unity UPM przez wersjonowany Git URL. APK, EXE i instalatory przez Releases.
Nie uruchamiaj publikacji automatycznie, jeśli naruszyłoby to ograniczenie zero-spend.
