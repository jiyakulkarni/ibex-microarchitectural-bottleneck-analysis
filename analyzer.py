# ============================================
# Ibex Trace Bottleneck Analyzer (CORRECT)
# ============================================

TRACE_FILE = (
    "../ibex_rtl/ibex/build/"
    "lowrisc_ibex_ibex_simple_system_0/"
    "sim-verilator/trace_core_00000000.log"
)

counts = {
    "total": 0,
    "load": 0,
    "store": 0,
    "branch": 0,
    "alu": 0,
}

last_load_rd = None
total_loads = 0
load_use_stalls = 0


def classify(decoded):
    d = decoded.lower()

    # LOAD
    if any(x in d for x in ["lw", "lh", "lb", "lhu", "lbu"]):
        if "sw" not in d:
            return "load"

    # STORE
    if any(x in d for x in ["sw", "sh", "sb"]):
        return "store"

    # BRANCH / JUMP
    if any(x in d for x in ["beq", "bne", "blt", "bge", "jal", "jalr", "c.j", "c.beq"]):
        return "branch"

    return "alu"


def extract_regs(decoded):
    decoded = decoded.replace(",", " ").replace("(", " ").replace(")", " ")
    toks = decoded.split()

    rd = rs1 = rs2 = None

    if len(toks) >= 2:
        rd = toks[1]
    if len(toks) >= 3:
        rs1 = toks[2]
    if len(toks) >= 4:
        rs2 = toks[3]

    return rd, rs1, rs2


# =============================
# Trace processing
# =============================

with open(TRACE_FILE) as f:
    next(f)  # skip header line

    for line in f:
        if not line.strip():
            continue

        parts = line.split()
        if len(parts) < 6:
            continue

        decoded = " ".join(parts[4:])

        instr_type = classify(decoded)
        rd, rs1, rs2 = extract_regs(decoded)

        counts["total"] += 1
        counts[instr_type] += 1

        # Load-use hazard detection
        if instr_type == "load":
            total_loads += 1
            last_load_rd = rd
        else:
            if last_load_rd is not None:
                if rs1 == last_load_rd or rs2 == last_load_rd:
                    load_use_stalls += 1
            last_load_rd = None


# =============================
# Metrics
# =============================

total = counts["total"]
loads = counts["load"]
stores = counts["store"]
branches = counts["branch"]

mpi = (loads + stores) / total if total else 0.0
branch_density = branches / total if total else 0.0
estimated_cpi = 1.0 + (2.0 * mpi) + (1.5 * branch_density)
ls_ratio = loads / (stores + 1e-9)
load_use_rate = load_use_stalls / total_loads if total_loads else 0.0


# =============================
# Output
# =============================

print("\nInstruction Breakdown")
print("----------------------")
for k, v in counts.items():
    print(f"{k:10s}: {v}")

print("\nBottleneck Metrics")
print("------------------")
print(f"Memory Pressure Index (MPI): {mpi:.3f}")
print(f"Branch Density            : {branch_density:.6f}")
print(f"Estimated CPI             : {estimated_cpi:.3f}")
print(f"Load / Store Ratio        : {ls_ratio:.2f}")

print("\nDependency Bottleneck")
print("---------------------")
print(f"Total Loads            : {total_loads}")
print(f"Load-Use Hazards       : {load_use_stalls}")
print(f"Load-Use Hazard Rate   : {load_use_rate:.3f}")
# ===============================
# CPI Component Breakdown Model
# ===============================

BASE_CPI = 1.0
MEM_PENALTY = 2.0      # assumed avg memory latency
BRANCH_PENALTY = 1.5   # assumed branch penalty

mem_cpi = MEM_PENALTY * mpi
branch_cpi = BRANCH_PENALTY * branch_density

print("\nCPI Breakdown")
print("-------------")
print(f"Base CPI              : {BASE_CPI:.2f}")
print(f"Memory Stall CPI      : {mem_cpi:.2f}")
print(f"Branch Penalty CPI    : {branch_cpi:.2f}")
print(f"Total Estimated CPI   : {BASE_CPI + mem_cpi + branch_cpi:.2f}")
# ===============================
# Cache-Aware CPI Modeling
# ===============================

print("\nCache-Aware CPI Analysis")
print("------------------------")

HIT_LAT = 1        # cache hit latency (cycles)
MISS_PENALTY = 15  # memory miss penalty (cycles)

for hit_rate in [0.0, 0.5, 0.8, 0.9, 0.95]:
    miss_rate = 1.0 - hit_rate

    mem_cpi_cache = mpi * (hit_rate * HIT_LAT + miss_rate * MISS_PENALTY)
    total_cpi = 1.0 + mem_cpi_cache + (branch_density * 1.5)

    print(f"Cache hit rate {hit_rate:4.2f} → CPI = {total_cpi:4.2f}")
print("\nWhat-if Memory Latency Study")
print("----------------------------")

for mem_lat in [1, 2, 3, 5]:
    cpi = 1.0 + mem_lat * mpi + branch_density * 1.5
    print(f"Memory latency {mem_lat} cycles → CPI = {cpi:.2f}")
