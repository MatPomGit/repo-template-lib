# Prywatność, pochodzenie danych i aparatury

Żadne rzeczywiste dane uczestników, nagrania, sekrety, zrzuty twarzy i wrażliwe wyniki nie należą do kodu Git.
W `config/component.json` podaj klasę danych i informacje, czy komponent działa offline, czy wysyła dane na serwer.
Rejestr urządzeń pomiarowych i kontraktów: `MatPomGit/research-autopilot/catalog/equipment/` i `docs/equipment/`.
Rejestr komputerów i sieci: `MatPomGit/homeserver-infra/docs/infrastructure/network/`.
Dla adapterów zachowaj `equipment_id`, typ/wersję SDK, jednostki, współrzędne, źródła timestampów, kalibrację, parametry i status pomiarowy.
Numer seryjny jest właściwością kanonicznego, kontrolowanego rejestru; nie publikuj go w publicznej dokumentacji bez decyzji właściciela.
