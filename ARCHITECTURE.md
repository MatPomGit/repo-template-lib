# Architektura biblioteki

**Status:** szablon nie zawiera gotowego produktu. Identyfikatory i komponenty należy zdefiniować przed implementacją.

- **Source of truth:** to repozytorium jest jedynym właścicielem kodu i publicznego kontraktu.
- **Upstream:** zależności przypięte do wersji i SHA/digest; aktualność sprawdzana przez Research Autopilot.
- **Downstream:** `msc-*` i inne narzędzia odwołują się do wydania lub ustalonego SHA, nie kopiują źródeł.
- **Boundary:** adaptery sprzętowe, rendering i I/O oddzielone od logiki domenowej, gdy dotyczy.
- **Reproduce:** zdefiniowany lockfile, wersje zależności i parametry.
- **Audit live:** odczyt aktualnego HEAD i porównanie z przypiętym SHA. Zmiany via PR, bez cichego nadpisywania.

Pełne kontrakty i macierz środowisk opisano w `docs/` i `config/component.json`.


## Dokumentacja rozwijanej biblioteki

Po powstaniu kodu opisz **realne** moduły, publiczne API, wersje ABI, granice I/O i adaptery w [components](docs/architecture/components.md), [data-flow](docs/architecture/data-flow.md) i [distribution](docs/architecture/distribution.md). [ADR](docs/adr/README.md) zapisują uzasadnienia decyzji, a [model zagrożeń](docs/security/threat-model.md) rzeczywiste ryzyka i dowody ich kontroli.

Publikacja dokumentacji jako GitHub Pages korzysta **wyłącznie** z `pages/`, nigdy z `docs/` ([polityka](docs/pages.md)). Brak wdrożonej funkcji oznacza stan `NOT_IMPLEMENTED`, a nie domyślny `PASS`.
