# Zarządzanie biblioteką

Właściciel odpowiada za uprawnienia, przyjęcie API, licencję i decyzję o dystrybucji. Autor implementacji zapewnia minimalny kod, testy i dokumentację, a niezależny recenzent ocenia finalny SHA. Praca agenta nie nadaje praw administracyjnych ani prawa do publikowania pakietów.

Kanoniczne API zapisuje się w `contracts/api.json`, SemVer w `config/component.json`, a kompatybilność konsumentów w dokumentacji i testach. Istotne wybory techniczne dokumentuj w [ADR](docs/adr/README.md), bez powielania kontraktów. Zmiany niekompatybilne wymagają planu migracji i dowodów.

[AGENTS.md](AGENTS.md) określa DoR/DoD, ryzyko R0–R3 i WIP. Sam merge nie jest wydaniem. Publikacja pakietu, Pages, wdrożenie i aktualizacje konsumentów mają odrębne bramki uprawnień. Zobacz [SECURITY.md](SECURITY.md) i [politykę Pages](docs/pages.md).
