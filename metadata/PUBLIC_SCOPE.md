# Ambito pubblico del Trentino-Alto Adige One Health AMR Atlas

Edizione `taa_amr_atlas`, pubblicata da Codex Vitae ETS. Il runtime carica soltanto le fonti `public_approved`.

La base pubblica comprende:

- confini ISTAT generalizzati al 1 gennaio 2026, letti in UTF-8: 282 comuni, 2 province autonome (Bolzano/Bozen, BZ 021; Trento, TN 022) e la regione 04. I nomi bilingui non sono ricodificati;
- sei indicatori AR-ISS 2024 per ciascuna provincia autonoma (sangue e liquor), con numerosità, percentuale e intervallo di confidenza. Copertura 100% in provincia di Bolzano e 85,6% in provincia di Trento. Licenza CC BY 4.0. CRAS ha meno di 20 isolati in entrambe le province. Nessun downscaling comunale;
- confezioni e spesa degli antibatterici J01 dagli Open Data AIFA 2024, distinte per provincia (convenzionata e acquisti diretti), CC BY 4.0: consumo, non resistenza e non DDD;
- rapporto ASUIT 2025 sul consumo territoriale di antibatterici per uso sistemico in Trentino (Tabella 1, DDD/1.000 abitanti/die 2019-2025), CC BY 4.0, scheda senza mappa. Attribuzione obbligatoria: «Fonte: sito dell'Azienda sanitaria universitaria integrata del Trentino - Provincia autonoma di Trento»;
- una struttura sanitaria nominata, georiferita con Nominatim il 20 novembre 2026 (ODbL 1.0, © OpenStreetMap contributors): Ospedale di Bolzano (San Maurizio);
- 23 studi con collegamento territoriale esplicito (20 novembre 2026), nei sei layer di evidenza. 20 studi riguardano la provincia di Bolzano/Bozen e 3 la provincia di Trento. Il layer umano ha 4 elementi e 19 studi. Il veterinario ha 1 elemento, l'alimentare 1, l'ambientale 2. Il layer della fauna selvatica è vuoto e il contorno regionale non raccoglie studi: nessuna evidenza pubblicata, non resistenza zero. Il segnaposto indica dove è stato condotto lo studio, non una prevalenza.

Non sono pubblicati i materiali ASDAA/SABES, lo studio ambientale dell'Agenzia per l'ambiente di Bolzano, il report veterinario ClassyFarm di TrentinoSalute, il cruscotto IZSVe né il PDF OsMed: vedi `EXCLUDED_SOURCES.md`. Non ci sono record individuali, identificativi di paziente o campione, né coordinate di RSA, aziende agricole, allevamenti o depuratori non nominati.
