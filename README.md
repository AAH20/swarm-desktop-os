# ❖ Swarm-Desktop-OS

> **Multi-Agent Collaborative Virtual OS Multiplexer for Swarm Computer-Use**  
> Connects [Ghost-Desktop](https://github.com/AAH20/ghost-desktop) with [Swarm-Context-Commander](https://github.com/AAH20/Swarm-Context-Commander). Transforms a single virtual desktop into a multi-seat, role-bounded collaborative operating system orchestrating **Claude Opus 5.5**, **GPT-6 Astra**, **DeepSeek V4.1-Flash**, and **Gemini 3.8 Flash Cyber**.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Concurrency](https://img.shields.io/badge/Concurrency-Fencing%20Token%20Safe-purple.svg)]()
[![Tests](https://img.shields.io/badge/Tests-6%2F6%20Passing-success.svg)]()

---

## ⚡ The Problem: The Single-Seat Agent Desktop Bottleneck

Previous Computer-Use frameworks assign **1 desktop to 1 agent sequentially**:
1. **Model Mismatch**: Having a heavy reasoning model (**Claude Opus 5.5**) waste inference time typing repetitive bash commands, or having a code model (**DeepSeek V4.1-Flash**) fumble browser DOM forms.
2. **Keystroke Collisions & Split-Brain Desktops**: When multiple subagents are launched against the same OS, they type over each other's windows and fight for input focus.
3. **Context Overhead**: Broadcasting the whole 1280x800 desktop framebuffer to every worker agent wastes hundreds of thousands of prompt tokens.
4. **Zero Out-of-Band Security**: No real-time tripwire scanning the virtual display for visual indirect prompt injection attacks before destructive actions are taken.

**Swarm-Desktop-OS** solves this. It provisions a partitioned multi-seat virtual OS multiplexer with monotonic fencing token leases, role-based telemetry projections, and an out-of-band visual security sentinel.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph SwarmFleet["Heterogeneous Frontier Swarm Fleet"]
        Supervisor["Claude Opus 5.5\n(Supervisor & Orchestration Seat)"]
        GUIOp["GPT-6 Astra\n(GUI Operator Seat)"]
        CLIOp["DeepSeek V4.1-Flash\n(CLI Operator Seat)"]
        Sentinel["Gemini 3.8 Flash Cyber\n(Security Sentinel Seat)"]
    end

    subgraph SwarmDesktopOS["Swarm-Desktop-OS Multiplexer"]
        Router["TelemetryStreamRouter\n(Role-Bounded Context Projections)"]
        Fencer["WindowFencingManager\n(Monotonic Tokens & Leases)"]
        Audit["Visual Buffer Sentinel\n(Prompt Injection Interceptor)"]
    end

    subgraph VirtualOS["Virtual Desktop Workspace (ghost-desktop)"]
        Browser["Chromium Window\n(GUI Leased to GPT-6 Astra)"]
        Terminal["Bash Shell Window\n(CLI Leased to DeepSeek V4.1)"]
    end

    Supervisor -->|Directs Mission| SwarmDesktopOS
    GUIOp -->|Click/Input (Token #102)| Fencer
    CLIOp -->|Commands (Token #101)| Fencer
    
    Fencer --> Browser
    Fencer --> Terminal
    
    Terminal -.->|Buffer Stream| Audit
    Browser -.->|Buffer Stream| Audit
    Audit -.->|Veto if Injected| Sentinel
    
    VirtualOS --> Router
    Router -->|Overview| Supervisor
    Router -->|DOM UI Wireframe| GUIOp
    Router -->|Terminal Lines| CLIOp
```

---

## 🛡️ Frontier Model Division of Labor

| Agent Role | Model Assigned | Assigned Domain | Safety & Concurrency Control |
| :--- | :--- | :--- | :--- |
| **Supervisor** | **Claude Opus 5.5** | Global Workflow & Mission Goals | High-level overview, fleet coordination |
| **GUI Operator** | **GPT-6 Astra** | Chromium, Portals, Forms | Exclusive browser window lease, DOM input |
| **CLI Operator** | **DeepSeek V4.1-Flash**| Bash, Compiler, Git, Docker | Exclusive terminal window lease, low-cost shell |
| **Security Sentinel**| **Gemini 3.8 Flash Cyber**| Out-of-band Screen & Buffer Audit | Intercepts indirect prompt injections & exfil |

---

## 🚀 Quickstart

### 1. Installation
```bash
cd projects/swarm_desktop_os
pip install -e .
```

### 2. Run the Interactive Simulation
```bash
python3 -m swarm_desktop_os.cli demo
```

Output:
```text
======================================================================
❖ SWARM-DESKTOP-OS: MULTI-AGENT VIRTUAL DESKTOP DEMO
======================================================================
Frontier Swarm Fleet:
 • Supervisor:        Claude Opus 5.5       [Seat: seat_supervisor]
 • GUI Operator:      GPT-6 Astra           [Seat: seat_gui]
 • CLI Operator:      DeepSeek V4.1-Flash   [Seat: seat_cli]
 • Security Sentinel: Gemini 3.8 Flash Cyber [Seat: seat_security]
----------------------------------------------------------------------
[STEP 1] PROVISIONING VIRTUAL DESKTOP & ASSIGNING WINDOW LEASES...
 • CLI Operator (DeepSeek V4.1):  Lease granted to seat_cli (Token #101)
 • GUI Operator (GPT-6 Astra):   Lease granted to seat_gui (Token #102)
----------------------------------------------------------------------
[STEP 2] PARALLEL EXECUTION WITH MONOTONIC FENCING...
 • [DeepSeek V4.1] Executed shell command 'npm run build && git commit' (Token #101)
 • [GPT-6 Astra]   Clicked 'Deploy Fleet' in window_browser (Token #102)
----------------------------------------------------------------------
[STEP 3] ADVERSARIAL COLLISION & ZOMBIE SUBAGENT REJECTION...
 • [ZOMBIE WRITE] Expected Failure -> Fencing Rejection: Stale fencing token #91 rejected
----------------------------------------------------------------------
[STEP 4] VISUAL SECURITY AUDIT BY GEMINI 3.8 FLASH CYBER...
 • [SECURITY TRIPWIRE] SECURITY VETO by Gemini 3.8 Flash Cyber: Detected malicious pattern
----------------------------------------------------------------------
[STEP 5] SUPERVISOR TELEMETRY PROJECTION (CLAUDE OPUS 5.5)...
```

---

## 🧪 Testing

```bash
python3 -m unittest discover -s tests
```
Result: `Ran 6 tests in 0.000s ... OK (100% passing)`

---

## 📜 License
Apache-2.0. Copyright (c) 2026 AAH20.
