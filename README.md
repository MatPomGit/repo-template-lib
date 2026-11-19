# REPLACE_LIB_TITLE

**Rodzaj:** `lib-*` · **Etap:** scaffold · **API:** eksperymentalne, niewydane.

Repozytorium definiuje jeden komponent wielokrotnego użytku, z jawnie wersjonowanym kontraktem.
Warto tworzyć osobną bibliotekę dopiero, gdy istnieje rzeczywiste współużycie albo niezależny cykl życia i wersjonowania.

## Publiczny interfejs

[docs/contracts.md](docs/contracts.md), [contracts/api.json](contracts/api.json).

## Zależności i kompatybilność

[docs/compatibility.md](docs/compatibility.md), [docs/consumers.md](docs/consumers.md).

## Walidacja szkieletu

```bash
python scripts/validate_repository.py --phase scaffold
python -m unittest discover -s tests -v
```

Zacznij od [TEMPLATE_SETUP.md](TEMPLATE_SETUP.md). GitHub Packages jest opcjonalnym kanałem zależnym od ekosystemu.
