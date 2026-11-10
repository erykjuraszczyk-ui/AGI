---
schema_version: 1.0.0
revision: 1
decision:
  id: ADR-001
  title: Modular cognitive core with ports and adapters
  status: accepted
  context: The AGI repository is an initial public project with only a minimal README in the inspected default-branch root. The user approved a Windows target and integration of Consciousness Core with Memory Core, Emotion Core, Perception Core, and Agent Runtime. There is no implementation evidence supporting a distributed deployment or a particular language.
  drivers:
    - Keep cognitive modules independently testable and replaceable.
    - Prevent direct coupling to storage, models, and Windows operating-system APIs.
    - Establish explicit governance for agent actions and memory lifecycle.
    - Support incremental delivery on Windows with limited initial complexity.
  considered_option_ids:
    - OPT-001
    - OPT-002
    - OPT-003
  selected_option_id: OPT-001
  decision: Adopt a modular monolith with ports and adapters for the first Windows implementation. Define explicit versioned contracts for Consciousness Core, Memory Core, Emotion Core, Perception Core, Agent Runtime, and Governance Core. Keep external model, persistence, device, and operating-system integrations behind adapters.
  positive_consequences:
    - Components can be tested independently through contract tests and deterministic adapters.
    - Initial deployment avoids distributed-systems overhead.
    - OS access and privileged actions can be centralized behind authorization boundaries.
  negative_consequences:
    - Module boundaries require discipline and automated checks to prevent internal coupling.
    - A single deployment unit may limit independent scaling until extraction is justified by measured needs.
    - The language and runtime remain unresolved and must be decided before implementation.
  assumptions:
    - Windows is the first target platform.
    - The repository is at an early stage and no hidden implementation is assumed from the minimal root listing.
    - The first release can run as one deployable application with logically separated modules.
    - Functional self-modeling is a product capability, not evidence of subjective consciousness.
  validation_criteria:
    - Each module exposes versioned public interfaces and passes independent contract tests.
    - Static dependency checks prevent Consciousness Core from directly accessing Windows APIs or persistence internals.
    - All privileged actions pass through Governance Core and produce audit events.
    - Memory records preserve provenance and user-controlled retention metadata.
    - Integrated tests demonstrate restart continuity from persisted state without claiming uninterrupted subjective experience.
  supersedes: []
---
# ADR-001: Modular cognitive core with ports and adapters

## Status
Accepted — explicitly approved by the user.

## Context
The AGI repository is an initial public project with only a minimal README in the inspected default-branch root. The user selected Windows and approved integration of Consciousness Core, Memory Core, Emotion Core, Perception Core, and Agent Runtime. There is no source-code evidence for a particular language or runtime.

## Considered options
- **OPT-001 — Modular monolith with ports and adapters:** one deployable application, explicit module ownership, versioned public interfaces, and adapters at external boundaries.
- **OPT-002 — Distributed services:** independently deployed modules communicating over network protocols.
- **OPT-003 — Layered monolith without explicit ports:** simpler initial structure but weaker isolation of external dependencies.

## Decision
Adopt OPT-001 — Modular monolith with ports and adapters for the first Windows implementation. Define explicit versioned contracts for all cognitive and governance modules. Keep external model, persistence, device, and Windows operating-system integrations behind adapters.

## Consequences
### Positive
- Components can be tested independently through contract tests and deterministic adapters.
- Initial deployment avoids distributed-systems overhead.
- OS access and privileged actions can be centralized behind authorization boundaries.

### Negative
- Module boundaries require discipline and automated checks to prevent internal coupling.
- A single deployment unit may limit independent scaling until extraction is justified by measured needs.
- Language and runtime remain unresolved and must be decided before implementation.

## Validation
- Public contracts are versioned and independently tested.
- Dependency checks prevent direct OS and persistence coupling from cognitive logic.
- Privileged actions are authorized and audited.
- Memory provenance and retention are testable.
- Restart continuity is based on persisted state, not claims of uninterrupted subjective experience.
