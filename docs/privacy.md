# Prywatność, pochodzenie danych i aparatury

Żadne rzeczywiste dane uczestników, nagrania, sekrety, zrzuty twarzy i wrażliwe wyniki nie należą do kodu Git.
Przed wdrożeniem biblioteki, która przetwarza dane osobowe lub komunikuje się z siecią, udokumentuj w tym repozytorium klasy danych, przepływy i network egress oraz wprowadź odpowiednie pola do schematu manifestu. Obecny `config/component.json` nie zawiera pól `data_classification` ani `network_egress`, dlatego nie traktuj ich jako zweryfikowanych.
Rejestr urządzeń pomiarowych i kontraktów: `MatPomGit/research-autopilot/catalog/equipment/` i `docs/equipment/`.
Rejestr komputerów i sieci: `MatPomGit/homeserver-infra/docs/infrastructure/network/`.
Dla adapterów zachowaj `equipment_id`, typ/wersję SDK, jednostki, współrzędne, źródła timestampów, kalibrację, parametry i status pomiarowy.
Numer seryjny jest właściwością kanonicznego, kontrolowanego rejestru; nie publikuj go w publicznej dokumentacji bez decyzji właściciela.
