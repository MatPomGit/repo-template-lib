# Standard dokumentacji i budżety znaków

Źródła prawdy są rozdzielone: [README](../README.md) opisuje produkt, [ARCHITECTURE](../ARCHITECTURE.md) granice, [moduły](architecture/components.md) implementację, [contracts/api.json](../contracts/api.json) publiczny interfejs, [ADR](adr/README.md) uzasadnienia, [SECURITY](../SECURITY.md) ochronę i zgłoszenia, [GOVERNANCE](../GOVERNANCE.md) odpowiedzialność, a [Pages](pages.md) zasady treści publicznych.

Limity w [config/documentation-policy.json](../config/documentation-policy.json) liczą **znaki Unicode** wraz z białymi znakami, nie bajty UTF-8.

| Dokument | Maksymalna liczba znaków |
| --- | ---: |
| `AGENTS.md`, `README.md`, `ARCHITECTURE.md` | 12 000 |
| `SECURITY.md` i procedura agentów | 10 000 |
| `CODE_OF_CONDUCT.md`, `SUPPORT.md`, ADR | 6 000–6 500 |
| `GOVERNANCE.md` | 7 000 |
| Rozdziały architektury i bezpieczeństwa | 8 500 |
| Lokalne `profiles/*/AGENTS.md` | 3 000 |
| Publiczne `pages/**/*.md` | 6 000 |

Walidację uruchamia `python scripts/validate_documentation.py` w CI. Przekroczenie limitu to `FAIL`. Najpierw usuń duplikaty, przenieś szczegóły do odpowiedniego dokumentu, utwórz jeden uzasadniony aneks. Nie zwiększaj arbitralnie limitu ani nie usuwaj istotnych informacji licencyjnych i bezpieczeństwa.

**Scaffold:** zachowaj `NOT_IMPLEMENTED`, `NOT_ASSESSED`, `NOT_RELEASED`. **Pierwszy moduł:** wprowadź rzeczywiste źródła, API, testy i diagram granic. **Pierwsze zależności/odbiorcy:** uzupełnij wersje, licencje, kompatybilność i ryzyka. **Przed release:** udokumentuj clean install, łańcuch dostaw, hash, testy i zgodę. **Przed publiczną witryną:** przygotuj tylko `pages/` z jawnie zatwierdzonymi zasobami i sprawdź wygenerowany HTML, widoczność i prawa. Nie umieszczaj na stronie poleceń dla agentów ani uwag redakcyjnych.

Budżety dotyczą dokumentacji Markdown, nie implementacji, danych i artefaktów. Obecność pliku nie zastępuje rzetelnego sprawdzenia jego treści.
