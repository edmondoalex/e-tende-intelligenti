## [0.1.3] - 2026-04-23
### Added
- Added integration icon assets (logo.png, docs image).

### Changed
- Bumped integration version to 0.1.3.

## [0.1.1] - 2026-04-23
### Added
- Prima versione funzionale con controllo cover basato su sole.
- Persistenza runtime per entry (`last_target_position`, `last_apply_at`) con restore al riavvio.
- Config flow + options flow completi per parametri per-singola-cover.
- Servizio `e_tende_intelligenti.apply_now` per applicazione immediata.
- Traduzioni/etichette UI (`strings.json`, `translations/it.json`).
- Guida tecnica estesa in `docs/COMPONENT_GUIDE.md`.

### Fixed
- Guardie runtime su valori non numerici o `None` (evita crash su sottrazioni invalide).

## [0.1.0] - 2026-04-23
### Added
- Inizializzazione repository Git.
- Struttura compatibile HACS (`hacs.json`).
- Scaffold integrazione Home Assistant in `custom_components/e_tende_intelligenti`.
- File di tracking sviluppo: `DEVELOPMENT_LOG.md`, `DECISIONS.md`, `ROADMAP.md`.
- README operativo con istruzioni installazione HACS.



