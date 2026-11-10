# AGI Cortana — Foundation Engine v0.1.0

Windows-first modular foundation for the Cortana AI agent.

> Functional self-modeling and introspection are software capabilities; they do not establish phenomenal consciousness or subjective experience.

## Requirements
- Python 3.12+
- Windows 10/11 (portable Python layer)
- Optional native bridge: CMake 3.20+, C++20 compiler, pybind11
- Optional API: install `.[api]`

## PowerShell setup
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,api,crypto]"
python -m pytest
python -m cortana.runtime.bootstrap
```

Run API locally:
```powershell
python -m uvicorn cortana.api.app:app --host 127.0.0.1 --port 8765
```
Do not expose the API beyond localhost until authentication and TLS are implemented.

## Included in v0.1.0
- Async in-process Event Bus
- Module Registry and lifecycle management
- Runtime health snapshot and optional HTTP endpoints
- Local/cloud model provider contracts and privacy-aware router
- Perception observation contract (no device capture)
- Default-deny governance policy
- AES-256-GCM encryption helper with externally managed key
- Optional C++20/pybind11 bridge
- Unit tests and Windows setup instructions

## Security boundaries
No shell execution, device activation, cloud network call, or production DPAPI key lifecycle is implemented. Sensitive requests are routed locally by policy. Keys must never be hard-coded or committed. Production Windows key management and recovery are a later milestone. Raw media is not persisted.

## Layout
- `src/cortana/runtime`: bootstrap, event bus, module registry, health.
- `src/cortana/contracts`: model and perception contracts.
- `src/cortana/ai_router`: privacy-aware provider selection.
- `src/cortana/governance`: default-deny authorization.
- `src/cortana/memory`: authenticated encryption primitive.
- `src/cortana/api`: optional localhost health API.
- `native`: optional C++20 extension.
