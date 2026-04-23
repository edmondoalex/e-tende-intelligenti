# Technical Decisions (ADR Light)

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
