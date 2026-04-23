## [0.1.10] - 2026-04-23
### Fixed
- Options flow robusto: se la cover salvata non esiste più, il form non va in errore 500.
- Unload sicuro del servizio `apply_now` con controllo `has_service` (niente warning "Unable to remove unknown service").
- Traduzione italiana `translations/it.json` corretta in UTF-8 valida.

## [0.1.9] - 2026-04-23
### Fixed
- Correzioni di stabilità su config flow/options flow.
- Migliorie naming profilo e gestione valori legacy.

## [0.1.1] - 2026-04-23
### Added
- Prima versione funzionale con controllo cover basato su sole.
- Persistenza runtime per entry (`last_target_position`, `last_apply_at`).
- Config flow + options flow.
- Servizio `e_tende_intelligenti.apply_now`.
