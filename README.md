# REPLACE_LIB_TITLE

**Rodzaj:** `lib-*` · **Etap:** scaffold · **API:** eksperymentalne, niewydane.  
**Autor podstawowy:** Mateusz Pomianek; opcjonalni współautorzy po potwierdzeniu wkładu.

Repozytorium definiuje jeden komponent wielokrotnego użytku, z jawnie wersjonowanym kontraktem.
Warto tworzyć osobną bibliotekę dopiero, gdy istnieje rzeczywiste współużycie albo niezależny cykl życia i wersjonowania.

## Publiczny interfejs

[docs/contracts.md](docs/contracts.md), [contracts/api.json](contracts/api.json).

## Zależności i kompatybilność

[docs/compatibility.md](docs/compatibility.md), [docs/consumers.md](docs/consumers.md).

## Walidacja szkieletu

```bash
python scripts/validate_repository.py --phase scaffold
python scripts/validate_documentation.py
python scripts/validate_pages.py
python -m unittest discover -s tests -v
```

Zacznij od [TEMPLATE_SETUP.md](TEMPLATE_SETUP.md). GitHub Packages jest opcjonalnym kanałem zależnym od ekosystemu.

## Audyt i kontrole jakości

Zobacz [audyt szablonu z 2026-11-19](reviews/2026-11-19-template-audit.md) i plan działań P0–P2. Publiczne repozytoria mogą korzystać z GitHub-hosted runners. Szablon zawiera minimalny [workflow Scaffold CI](.github/workflows/ci.yml) z walidacją metadanych i testami regresyjnymi; nie buduje ani nie publikuje pakietów.

## Architektura i bezpieczeństwo

[Architektura](ARCHITECTURE.md), [ADR](docs/adr/README.md), [model zagrożeń](docs/security/threat-model.md), [łańcuch dostaw](docs/security/supply-chain.md), [zarządzanie](GOVERNANCE.md) i [limity dokumentacji](docs/documentation.md). Publiczne Pages korzysta tylko z `pages/`; `docs/` pozostaje wewnętrzne.
