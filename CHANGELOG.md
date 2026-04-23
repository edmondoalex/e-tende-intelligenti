## [0.1.11] - 2026-04-23
### Fixed
- Risolto errore 500 nel flow opzioni quando la cover salvata non esiste più (`cover_entity` required senza `default=None`).

## [0.1.10] - 2026-04-23
### Fixed
- Options flow robusto con gestione cover non più presente.
- Unload sicuro del servizio `apply_now` con controllo `has_service`.
- Traduzione italiana `it.json` corretta (UTF-8 valida).

## [0.1.9] - 2026-04-23
### Fixed
- Correzioni stabilità config flow/options flow.
- Migliorie naming profilo e valori legacy.

## [0.1.1] - 2026-04-23
### Added
- Prima versione funzionale con controllo cover basato sul sole.
- Persistenza runtime per entry.
- Config flow + options flow.
- Servizio `e_tende_intelligenti.apply_now`.
