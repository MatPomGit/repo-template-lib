# Polityka GitHub Actions w repozytoriach `lib-*`

Publiczne repozytoria mogą wykorzystywać **GitHub-hosted runners** (np. `ubuntu-latest`) do bezpiecznych i izolowanych testów `pull_request` i `push`. Nie wymagaj uruchamiania zwykłego CI na stałym runnerze. Uwzględnij limity usługi, koszty i zasadę braku dodatkowych wydatków bez zgody. W repozytoriach prywatnych zdecyduj osobno, biorąc pod uwagę politykę danych i rozliczanie runnera.

Szablon **nie zawiera jeszcze workflowów**. Zalecany minimalny zestaw to walidacja `python scripts/validate_repository.py --phase scaffold`, `python -m unittest discover -s tests -v`, kontrola metadanych oraz przyszły test kontraktu API. Samo zapisanie tych poleceń nie jest dowodem wykonania.

Dla niezaufanych PR stosuj `permissions: contents: read` i nie przekazuj sekretów. Nie używaj `pull_request_target` do wykonywania kodu z forków ani nie uruchamiaj takiego kodu na zaufanych stałych runnerach. Buildy wymagające prywatnych zależności lub dostępu do zasobów chronionych wykonuj oddzielnie po autoryzacji.

Publikacja pakietu do rejestru, tworzenie Releases i deployment Pages wymagają osobnego zatwierdzenia. Plan wdrożenia CI i kontroli wydania jest w [audycie](../reviews/2026-11-19-template-audit.md).
