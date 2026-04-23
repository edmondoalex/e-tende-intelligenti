# e-Tende Intelligenti

![e-Tende Intelligenti](docs/assets/e-tende-intelligenti.png)

Custom integration Home Assistant (HACS) per controllo tapparelle/tende basato sulla posizione del sole, con configurazione semplice per singola cover.

## Stato attuale
- Release corrente: `0.1.4`
- Installazione: HACS (`Integration`)
- Configurazione: completamente da UI (Config Flow + Options Flow)
- Persistenza: configurazione + stato runtime minimo persistenti al riavvio

## Funzioni disponibili (v0.1.4)
- 1 entry = 1 cover gestita
- Calcolo posizione target da `sun.sun` (`azimuth` + `elevation`)
- Finestra angolare con `window_azimuth`, `fov_left`, `fov_right`
- Range attivo con `min_elevation`, `max_elevation`
- Posizioni dedicate:
  - `default_position` (sole non utile)
  - `sunset_position` (dopo tramonto)
- Limiti operativi: `min_position`, `max_position`
- Antirumore: `min_delta` + `interval_minutes`
- Servizio manuale: `e_tende_intelligenti.apply_now`

## Installazione HACS
1. HACS -> `Integrations` -> menu `...` -> `Custom repositories`
2. Repository: `https://github.com/edmondoalex/e-tende-intelligenti`
3. Categoria: `Integration`
4. Installa e seleziona tag più recente (`v0.1.4`)
5. Riavvia Home Assistant

## Parametri principali
- `cover_entity`
- `window_azimuth`
- `fov_left` / `fov_right`
- `min_elevation` / `max_elevation`
- `default_position` / `sunset_position`
- `min_position` / `max_position`
- `min_delta`
- `interval_minutes`
- `enabled`

## Guida completa
- [docs/COMPONENT_GUIDE.md](docs/COMPONENT_GUIDE.md)

## Tracking sviluppo
- [CHANGELOG.md](CHANGELOG.md)
- [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md)
- [DECISIONS.md](DECISIONS.md)
- [ROADMAP.md](ROADMAP.md)
