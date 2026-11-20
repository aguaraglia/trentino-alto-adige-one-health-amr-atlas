# Geografia pubblica

La cartografia pubblica dell'edizione Trentino-Alto Adige comprende:

- `atlas_region.geojson`: confine regionale ISTAT 2026 (codice 04);
- `atlas_provinces.geojson`: 2 province autonome ISTAT 2026, Bolzano/Bozen (BZ 021) e Trento (TN 022);
- `atlas_municipalities.geojson`: 282 comuni ISTAT al 1/1/2026.

I file sono letti in UTF-8 dal DBF ISTAT, quindi i nomi bilingui (per esempio Bolzano/Bozen) sono corretti.

Gli studi della letteratura curata stanno in layer distinti sotto `public/data/`. Una sola struttura nominata è geocodificata: l'Ospedale di Bolzano, tramite OSM Nominatim. Gli studi su Bolzano città usano il poligono del comune; quelli provinciali usano il poligono della provincia autonoma. Nessuna RSA, azienda agricola, depuratore o struttura non nominata è localizzata.
