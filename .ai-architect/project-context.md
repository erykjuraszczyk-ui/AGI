# Project Context — AGI Cortana

## Repository
- Repository: https://github.com/erykjuraszczyk-ui/AGI
- Default branch: main
- Visibility: public
- Platform target: Windows
- Observed baseline: repository root currently contains README.md only; README says "AGI Cortana".
- Evidence limitation: no application source, build configuration, tests, or existing architecture artifacts were present in the inspected root listing.

## Product intent
Build Cortana as a modular AI agent with a functional self-model, introspection, metacognition, persistent memory, emotion-state modeling, perception, and controlled task execution.

## Approved architectural direction
Use a modular monolith initially, with explicit ports-and-adapters boundaries between:
- Consciousness Core
- Memory Core
- Emotion Core
- Perception Core
- Agent Runtime
- Governance Core

The Consciousness Core owns the functional self-model and reflection orchestration; it does not claim or prove phenomenal consciousness.

## Constraints and assumptions
- Windows is the initial target platform.
- Existing implementation language and framework are unknown.
- Modules must communicate through versioned interfaces rather than direct database or operating-system coupling.
- Persistent user data must be transparent, access-controlled, and deletable according to policy.
- Self-modification is out of scope for runtime autonomy; code changes require isolated proposal, tests, security review, and explicit human approval.
- No claim of subjective experience, sentience, biological consciousness, or soul may be made without evidence.

## Initial quality priorities
1. Safety and authorization boundaries.
2. Data integrity and recoverable memory.
3. Observability and diagnosability.
4. Modularity and testability.
5. Clear distinction between observed facts, inferences, and unknowns.

## Known unresolved questions
- Runtime and primary implementation language.
- Whether local inference is required, and which model/runtime will be used.
- Whether speech, camera, and sensor perception are in the first release.
- Data retention, encryption, and backup requirements.
- Whether components will remain in one process initially or need separate processes.
