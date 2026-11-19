# Architektura biblioteki

**Status:** szablon nie zawiera gotowego produktu. Identyfikatory i komponenty należy zdefiniować przed implementacją.

- **Source of truth:** to repozytorium jest jedynym właścicielem kodu i publicznego kontraktu.
- **Upstream:** zależności przypięte do wersji i SHA/digest; aktualność sprawdzana przez Research Autopilot.
- **Downstream:** `msc-*` i inne narzędzia odwołują się do wydania lub ustalonego SHA, nie kopiują źródeł.
- **Boundary:** adaptery sprzętowe, rendering i I/O oddzielone od logiki domenowej, gdy dotyczy.
- **Reproduce:** zdefiniowany lockfile, wersje zależności i parametry.
- **Audit live:** odczyt aktualnego HEAD i porównanie z przypiętym SHA. Zmiany via PR, bez cichego nadpisywania.

Pełne kontrakty i macierz środowisk opisano w `docs/` i `config/component.json`.
