# Development Log

## 2026-04-23 (sessione 13)
- Fix definitivo del 500 su ingranaggio (options flow): rimosso `default=None` dal campo required `cover_entity`.
- Patch applicata su HA `3.24` e allineata al repository.

## 2026-04-23 (sessione 12)
- Fix su `3.24`: unload servizio con guardia `has_service`.
- Correzione JSON/encoding traduzioni.
- Verifica entry e cover salvata in `.storage/core.config_entries`.

## 2026-04-23 (sessioni precedenti)
- Bootstrap integrazione, config flow, scheduler, persistenza runtime, servizio `apply_now`.
- Hardening progressivo su flow opzioni e compatibilità HACS.
