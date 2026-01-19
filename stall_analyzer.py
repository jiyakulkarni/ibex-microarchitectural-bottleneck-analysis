trace_file = "trace_core_00000000.log"

stall = {
    "IF": 0,
    "ID": 0,
    "EX": 0,
    "MEM": 0
}

prev_cycle = None
prev_pc = None

with open(trace_file) as f:
    for line in f:
        if not line.strip() or line.startswith("Time"):
            continue

        parts = line.split()
        try:
            cycle = int(parts[1])
            pc = int(parts[2], 16)
        except:
            continue

        if prev_cycle is not None:
            delta = cycle - prev_cycle

            if delta > 1:
                stall_cycles = delta - 1

                if pc == prev_pc:
                    stall["MEM"] += stall_cycles
                elif pc != prev_pc:
                    stall["EX"] += stall_cycles

        prev_cycle = cycle
        prev_pc = pc

print("\nPipeline Stall Attribution")
print("--------------------------")
total_stall = sum(stall.values())

for k, v in stall.items():
    pct = (v / total_stall * 100) if total_stall > 0 else 0
    print(f"{k:4s} stall cycles : {v:8d} ({pct:5.1f}%)")
