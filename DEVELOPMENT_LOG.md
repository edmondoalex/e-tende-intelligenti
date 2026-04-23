# Development Log

## 2026-04-23 (sessione 4)`r`n- Aggiunta icona progetto: `custom_components/e_tende_intelligenti/logo.png`.
- Richiesta utente: tutto persistente ad ogni riavvio.
- Implementata persistenza runtime per entry su Home Assistant Store:
  - `last_target_position`
  - `last_apply_at`
- Caricamento automatico runtime in `async_start` e salvataggio su stop/apply.

## 2026-04-23 (sessione 2)
- Richiesta utente: UI config flow semplice + documentazione chiara funzionamento componente.
- Implementato controller reale `ETendeCoverController` con:
  - calcolo posizione target da `sun.sun`
  - controllo in-front con azimuth/fov
  - range elevazione
  - fallback default/sunset
  - antirumore su `min_delta`
  - scheduler periodico `interval_minutes`
- Implementato `config_flow` e `options_flow` con tutti i parametri principali.
- Implementato servizio `e_tende_intelligenti.apply_now`.
- Aggiunte traduzioni UI (`strings.json`, `translations/it.json`).
- Aggiunta guida tecnica `docs/COMPONENT_GUIDE.md`.

## 2026-04-23 (sessione 1)
- Bootstrap progetto `e-Tende Intelligenti`.
- Creato repo Git locale.
- Impostata struttura HACS installabile.
- Aggiunto scaffold custom component HA (manifest, init, const, config_flow placeholder).
- Aggiunto sistema documentale per tracciamento evoluzione tecnica.

## Prossimo step suggerito
- Test in HA reale di una entry su cover sala.
- Aggiunta entita diagnostiche (sun_in_front, target_position, last_apply).
- Introduzione manual override robusto e profilo BUSPRO-safe.


