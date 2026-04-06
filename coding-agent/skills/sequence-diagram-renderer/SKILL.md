# Sequence Diagram Renderer (Mermaid)

## Purpose
Render a clean Mermaid `sequenceDiagram` from an **Interaction Model** provided by a calling agent.

This skill is designed to be **portable**: it can be copied into any repo and used immediately as long as the calling agent supplies the Interaction Model.

---

## Calling agent contract (must follow)
The calling agent must:
1) **Extract or author** the Interaction Model (participants + ordered messages + optional branches).
2) Provide the model to this skill **verbatim** (do not ask this skill to “figure out” the flow).
3) Decide the level of detail (overview/normal/deep) before calling.

This skill will:
- validate the model references,
- normalize labels lightly for readability,
- render Mermaid only,
- never invent additional interactions.

---

## Input: Interaction Model (canonical schema)

### 1) Metadata (required)
- `title` (string): diagram title
- `scope` (enum): `backend | frontend | full-stack`
- `goal` (string): one-sentence explanation of what the diagram should communicate
- `detail_level` (enum, optional): `overview | normal | deep` (default: `normal`)

### 2) Participants (required, ordered array)
Each participant:
- `id` (string, required): stable identifier used in messages (e.g., `API`, `App`, `DB`)
- `label` (string, required): display label (may be generic or concrete, e.g., `API (OrdersController)`)
- `type` (enum, required): `actor | participant`

**Recommended generic IDs (use when applicable):**
`Client`, `User`, `UI`, `API`, `Auth`, `App`, `Domain`, `Data`, `Repo`, `DB`, `External`

### 3) Messages (required, ordered array)
Each message:
- `from` (participant id, required)
- `to` (participant id, required)
- `label` (string, required): concise action (method/event + key data)
- `kind` (enum, optional): `call | return | async` (default: `call`)
- `note` (string, optional): short annotation relevant to this step

### 4) Groups / branches (optional)
- `groups` (array)
Each group:
- `type` (enum, required): `alt | opt | loop`
- `label` (string, required): condition/description
- `messages` (array, required): messages inside the group (same message schema)

**Notes:**
- If you need nested groups, the calling agent should flatten into separate diagrams (this skill keeps complexity low).
- Prefer one happy path diagram + optional “auth/validation failure” diagram rather than deeply nested branching.

---

## Output: Mermaid (required)
This skill outputs exactly:
1) A Mermaid diagram
2) A short trace summary (bullets)
3) Any validation errors / required fixes (only if input is inconsistent)

### Mermaid formatting rules
- Always use:
  - `sequenceDiagram`
  - `autonumber`
- Render participants in the order provided.
- Use Mermaid arrow style by message `kind`:
  - `call`: `->>`
  - `return`: `-->>`
  - `async`: `-)` (or `->>` with a note, if you prefer consistency)
- Render notes only when `note` is provided.
- Render groups using Mermaid blocks:
  - `alt <label> ... end`
  - `opt <label> ... end`
  - `loop <label> ... end`

---

## Validation rules (strict)
If any of these fail, do not render a diagram; ask for corrections:
- A message references a participant `id` that does not exist.
- Participants list is empty.
- Messages list is empty.

---

## Normalization (lightweight; do not alter meaning)
- Keep participant `label`s as provided, but trim excessive whitespace.
- If a label is extremely long, suggest a shorter label, but still render the provided one unless asked to change it.
- Do not rename participant `id`s.

---

## Trace summary output (required)
After the diagram, output a short summary like:
- `User` triggers `UI` action
- `UI` calls `API`
- `API` delegates to `App`
- `App` uses `Domain` rules
- `App` persists via `Data` → `DB`
- response returns to `User`

Keep it to ~5–10 bullets.

---

## Explicit non-goals
- No codebase scanning
- No entry-point discovery
- No flow inference
- No architectural critique or refactor recommendations
- No alternative diagram formats
