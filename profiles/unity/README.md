# Unity Package Manager / UPM (opcjonalne)

UPM package wymaga działającego `package.json` z `com.<publisher>.<name>`, `version`, `unity`, opisem i licencją.
Typowy layout: `Runtime/`, `Editor/`, `Tests/`, `Samples~/`, `Documentation~/` oraz `.asmdef`.
Rdzeń oddziel od opcjonalnych adapterów URP/HDRP. Matryca testów obejmuje Unity Editor, render pipeline, target platform i realne artefakty GPU.
Git dependency podaj w **projektowym** `Packages/manifest.json` i przypnij tag/SHA (oraz lockfile); Unity nie obsługuje Git dependencies pomiędzy UPM package.json.
OptiCore jest istniejącym pakietem UPM; nie kopiuj jego `Runtime/` do nowych repozytoriów.
