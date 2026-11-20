# Polityka GitHub Actions w repozytoriach `lib-*`

Publiczne repozytoria mogą wykorzystywać **GitHub-hosted runners** (np. `ubuntu-latest`) do bezpiecznych i izolowanych testów `pull_request` i `push`. Nie wymagaj uruchamiania zwykłego CI na stałym runnerze. Uwzględnij limity usługi, koszty i zasadę braku dodatkowych wydatków bez zgody. W repozytoriach prywatnych zdecyduj osobno, biorąc pod uwagę politykę danych i rozliczanie runnera.

Szablon zawiera `.github/workflows/ci.yml` uruchamiający `python scripts/validate_repository.py --phase scaffold` oraz `python -m unittest discover -s tests -v` dla PR i push na `main`. W repo prywatnych job jest domyślnie pomijany i wymaga świadomej konfiguracji. Są to kontrole struktury i deklarowanego kontraktu API, **nie** test budowy i dystrybucji pakietu ani zgoda na publikację. Rzeczywiste wykonanie weryfikuj w GitHub Actions; same polecenia w YAML nie są dowodem `PASS`.

Dla niezaufanych PR stosuj `permissions: contents: read` i nie przekazuj sekretów. Nie używaj `pull_request_target` do wykonywania kodu z forków ani nie uruchamiaj takiego kodu na zaufanych stałych runnerach. Buildy wymagające prywatnych zależności lub dostępu do zasobów chronionych wykonuj oddzielnie po autoryzacji.

Publikacja pakietu do rejestru, tworzenie Releases i deployment Pages wymagają osobnego zatwierdzenia. Plan wdrożenia CI i kontroli wydania jest w [audycie](../reviews/2026-11-19-template-audit.md).

Walidatory `scripts/validate_documentation.py` i `scripts/validate_pages.py` działają offline w istniejącym jobie. Środowisko nie wymaga tokenu publikacyjnego, a wdrożenie GitHub Pages i wydanie do registry pozostają osobno zatwierdzanymi działaniami. Wynik statycznego skanu nie zastępuje oceny wygenerowanego HTML i poufności.
