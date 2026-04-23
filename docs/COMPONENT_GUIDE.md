# Guida componente e-Tende Intelligenti

## Obiettivo
Gestire tapparelle/tende in modo adattivo in base al sole, con impostazioni semplici per ogni singola cover da UI Home Assistant.

## Come funziona (v0.1.1)
Per ogni config entry:
1. legge lo stato di `sun.sun` (azimuth, elevation, below/above horizon)
2. calcola se il sole e "davanti" alla finestra con `window_azimuth` + `fov_left/right`
3. se sole in fronte e in range elevazione, calcola una posizione target tra `min_position` e `max_position`
4. se sole non in fronte o fuori range, usa `default_position`
5. se e tramonto/notte (`sun.sun == below_horizon`), usa `sunset_position`
6. applica la posizione solo se la differenza supera `min_delta`
7. riesegue ogni `interval_minutes`

## Parametri UI (config flow)
- `cover_entity`: entita cover da controllare.
- `window_azimuth`: direzione finestra (N=0, E=90, S=180, O=270).
- `fov_left` / `fov_right`: apertura angolare rispetto al centro finestra.
- `min_elevation` / `max_elevation`: range verticale del sole in cui intervenire.
- `default_position`: posizione quando non c'e sole utile davanti.
- `sunset_position`: posizione dopo il tramonto.
- `min_position` / `max_position`: limiti di lavoro durante sole in fronte.
- `min_delta`: variazione minima per evitare micro-movimenti.
- `interval_minutes`: intervallo minimo tra applicazioni.
- `enabled`: abilita/disabilita automazione per entry.

## Servizio disponibile
- `e_tende_intelligenti.apply_now`
  - forza il calcolo/applicazione immediata.
  - campo opzionale `entry_id` per applicare a una sola entry.

## Persistenza al riavvio
- Configurazione entry e opzioni: persistenti via Config Entries Home Assistant.
- Runtime minimo persistente per entry in `.storage`:
  - `last_target_position`
  - `last_apply_at`
- Al riavvio il controller ricarica automaticamente questi dati.

## Note robustezza
- Gestione valori non numerici/None su azimuth, elevation e current_position.
- Nessun calcolo su stati non validi.

## Tuning rapido consigliato
- base: `fov 70/70`, `min_elevation 8`, `max_elevation 65`, `min_delta 3`, `interval 5`
- se muove troppo: alza `min_delta` o `interval`
- se interviene presto/tardi: correggi `window_azimuth` ±5/10°

## Limitazioni attuali
- Nessuna logica manual override avanzata (arriva in milestone successiva).
- Nessuna gestione blindspot dedicata (arriva in milestone successiva).

