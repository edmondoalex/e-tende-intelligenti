# Technical Decisions (ADR Light)

## 2026-04-23 - Persistenza esplicita runtime
**Decisione**: salvare stato runtime minimo per ogni entry in `.storage` (non solo config flow/options).

**Motivazione**:
- Reboot-safe operativo.
- Traccia diagnostica coerente tra sessioni.

**Conseguenze**:
- Scritture leggere periodiche su storage.
- Ripresa piu prevedibile dopo restart.

---
## 2026-04-23 - Configurazione per-singola-cover in UI
**Decisione**: ogni config entry controlla una singola cover con parametri completi modificabili via options flow.

**Motivazione**:
- UX semplice e diretta in Home Assistant.
- Taratura indipendente per ogni finestra/tapparella.

**Conseguenze**:
- Piu entry se ci sono molte cover.
- Maggiore chiarezza operativa in manutenzione.

---

## 2026-04-23 - Guardie anti-None nel calcolo
**Decisione**: introdurre conversioni sicure (`_safe_float/_safe_int`) e fallback immediati su valori non validi.

**Motivazione**:
- Evitare crash runtime tipo `TypeError` su operazioni con `None`.
- Maggiore resilienza con cover/integrazioni rumorose.

**Conseguenze**:
- Alcuni cicli possono saltare applicazione quando i dati non sono affidabili.
- Stabilita generale migliore.

---

## 2026-04-23 - Bootstrap HACS first
**Decisione**: partire da una base minima installabile da HACS prima di portare la logica avanzata.

**Motivazione**:
- Riduce tempi di feedback su installazione/release.
- Evita sviluppo funzionale su base non distribuibile.

**Conseguenze**:
- Versione iniziale priva di logica business completa.
- Necessario un secondo step per funzionalita adattive.

---

## 2026-04-23 - Documentazione di processo obbligatoria
**Decisione**: mantenere file storici dedicati (`CHANGELOG`, `DEVELOPMENT_LOG`, `ROADMAP`, `DECISIONS`).

**Motivazione**:
- Tracciabilita tecnica.
- Continuita tra sessioni e release.

**Conseguenze**:
- Overhead minimo di manutenzione documentale ad ogni incremento.

