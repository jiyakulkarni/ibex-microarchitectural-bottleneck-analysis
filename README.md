# Cycle-Accurate Microarchitectural and Pipeline Bottleneck Analysis of the Ibex RISC-V Core

This project presents a cycle-accurate microarchitectural and pipeline-level bottleneck analysis of the Ibex RISC-V core using RTL instrumentation, execution tracing, and real bare-metal software workloads.

The objective is to understand performance-limiting factors such as memory stalls, pipeline hazards, and CPI contributors directly from RTL-level behavior rather than high-level simulators.

---

## Key Contributions

- Cycle-accurate execution tracing using Verilator
- RTL-level CPI and performance counter instrumentation
- Five-stage pipeline behavior analysis
- Pipeline stall attribution (IF, ID, EX, MEM stages)
- Memory pressure and dependency bottleneck analysis
- Cache-aware and memory latency what-if CPI modeling
- Analysis using real bare-metal RISC-V workloads
- Waveform-backed validation using GTKWave

---

## Analysis Overview

### Instruction Mix Analysis
- Load, store, branch, and ALU instruction breakdown
- Memory pressure index (MPI)
- Load to store ratio

### CPI Breakdown
- Base CPI
- Memory stall CPI
- Branch penalty CPI
- Total estimated CPI

### Pipeline Stall Attribution
Stalls are classified using cycle-accurate timing into:
- Instruction Fetch (IF) stalls
- Decode (ID) stalls
- Execute (EX) stalls
- Memory (MEM) stalls

### What-If Studies
- Memory latency impact on CPI
- Cache hit-rate sensitivity analysis

---

## Tools and Environment

- Ibex RISC-V Core
- Verilator (cycle-accurate simulation)
- GTKWave (waveform analysis)
- Python (trace parsing and bottleneck analysis)
- FuseSoC
- Bare-metal RISC-V software

---

## Repository Structure

