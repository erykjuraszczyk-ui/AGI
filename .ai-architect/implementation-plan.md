# Architecture-Driven Implementation Plan

## Accepted decisions
- ADR-001: Modular monolith with ports and adapters for the initial Windows implementation.
- Architecture contract revision: 1.
- Consciousness Core integrates with Memory Core, Emotion Core, Perception Core, and Agent Runtime only through versioned public interfaces.
- This plan describes implementation work; no application code has been changed by this architecture handoff.

## Milestones

### M1 — Repository and runtime foundation
- Outcome: Establish a reproducible Windows development environment and module skeleton.
- Scope: Repository layout, dependency management, configuration, logging, health endpoint, CI baseline.
- Constraints: Do not assume a language until Q-001 is resolved; keep secrets out of source control.
- Dependencies: Q-001.
- Verification: Clean environment setup succeeds; CI validates formatting, static checks, and unit tests.

### M2 — Shared contracts and Governance Core
- Outcome: Define versioned request/response schemas, error taxonomy, authorization decisions, and audit events.
- Scope: Contract package, policy interface, approval records, audit sink.
- Constraints: Default-deny privileged operations; no cognitive module has direct OS access.
- Dependencies: M1.
- Verification: Contract tests cover allowed, denied, malformed, expired, and replayed requests.

### M3 — Memory Core
- Outcome: Implement working, episodic, semantic, and identity memory with provenance and lifecycle controls.
- Scope: Persistence port, repositories, schemas, indexing interface, export/correction/deletion.
- Constraints: Explicit retention policy; encryption at rest where supported; user controls for stored data.
- Dependencies: M1, M2, Q-004.
- Verification: Round-trip, provenance, migration, deletion, backup/restore, and access-control tests.

### M4 — Functional Self Model
- Outcome: Implement identity manifest, capability registry, limitation registry, active-state snapshot, and uncertainty ledger.
- Scope: Consciousness Core domain model and introspection interfaces.
- Constraints: Runtime facts must come from telemetry or subsystem contracts; no unsupported consciousness claims.
- Dependencies: M2, M3.
- Verification: Tests distinguish observed state, inference, hypothesis, and unknown; restart reconstructs only persisted state.

### M5 — Emotion and Perception adapters
- Outcome: Integrate affect estimates and normalized sensory observations.
- Scope: Emotion Core and Perception Core ports/adapters, modality metadata, consent and permission checks.
- Constraints: Emotion outputs are estimates; raw media retention is off unless explicitly configured.
- Dependencies: M2, Q-002, Q-003, Q-004.
- Verification: Missing, low-confidence, contradictory, and revoked-consent inputs are handled safely.

### M6 — Agent Runtime integration
- Outcome: Connect task planning and action execution to self-monitoring and governance.
- Scope: Task lifecycle, action proposals, authorization, cancellation, timeout, idempotency, result telemetry.
- Constraints: No direct action from raw perception; privileged actions require policy authorization.
- Dependencies: M2, M4, M5.
- Verification: Denied actions have no side effects; cancellation, retries, timeout, and audit traces behave predictably.

### M7 — Validation and hardening
- Outcome: Verify integrated behavior, privacy, resilience, and operational readiness.
- Scope: Integration tests, threat model, resource limits, backup/restore drills, Windows packaging.
- Constraints: No claim of phenomenal consciousness based on functional tests.
- Dependencies: M3–M6.
- Verification: Acceptance suite passes; documented limitations and unresolved questions are reviewed.

## Cross-cutting constraints
- Keep module ownership explicit; communicate through contracts, not shared internal tables.
- Apply least privilege to Windows capabilities and isolate external tools.
- Validate all model-generated arguments and treat model output as untrusted.
- Preserve provenance and confidence semantics for memories and observations.
- Provide structured logs without leaking secrets, raw personal data, or unnecessary media.
- Make user data export, correction, and deletion testable.
- Require human approval for deployment, policy changes, and self-modification of production code.

## Explicit non-goals
- Proving or claiming machine phenomenal consciousness, sentience, or subjective feeling.
- Unrestricted autonomous control of Windows.
- Unsupervised self-modification of production software or security policy.
- Multi-host distributed services in the first implementation phase unless later evidence requires them.
- Retaining raw audio/video by default.

## Unresolved questions
- Q-001 (blocks M1): primary language and runtime.
- Q-002 (affects M5): mandatory offline/local inference requirement.
- Q-003 (affects M5): first-release perception modalities.
- Q-004 (blocks production persistence design): retention, encryption, backup, and recovery requirements.
