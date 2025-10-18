import pcbnew
import csv
import json

board = pcbnew.GetBoard()
nets = {}

# --- Collect all pads grouped by net ---
for pad in board.GetPads():
    netname = pad.GetNetname()
    if not netname:
        continue

    parent = pad.GetParent()
    try:
        ref = parent.GetReference()
    except AttributeError:
        ref = getattr(parent, "m_Parent", None)
        if ref and hasattr(ref, "GetReference"):
            ref = ref.GetReference()
        else:
            ref = "UNKNOWN"

    pin = pad.GetPadName()
    pos = pad.GetPosition()
    x = round(pcbnew.ToMM(pos.x), 3)
    y = round(pcbnew.ToMM(pos.y), 3)
    side = "Front" if pad.IsOnLayer(pcbnew.F_Cu) else "Back"

    if netname not in nets:
        nets[netname] = []
    nets[netname].append({
        "component": ref,
        "pin": pin,
        "x_mm": x,
        "y_mm": y,
        "side": side
    })

# --- Print summary ---
print(f"\n✅ Extracted {len(nets)} nets from: {board.GetFileName()}")

# --- Save JSON grouped by net ---
json_path = board.GetFileName().replace(".kicad_pcb", "_netlist_grouped.json")
with open(json_path, "w") as jf:
    json.dump(nets, jf, indent=2)
print(f"💾 JSON saved: {json_path}")

# --- Save CSV grouped by net ---
csv_path = board.GetFileName().replace(".kicad_pcb", "_netlist_grouped.csv")
rows = []
for net, pins in nets.items():
    for p in pins:
        rows.append([net, p["component"], p["pin"], p["x_mm"], p["y_mm"], p["side"]])

rows.sort(key=lambda r: r[0])
with open(csv_path, "w", newline="") as cf:
    writer = csv.writer(cf)
    writer.writerow(["Net", "Component", "Pin", "X(mm)", "Y(mm)", "Side"])
    writer.writerows(rows)
print(f"💾 CSV saved: {csv_path}")

# --- Integer TXT export (x10 scaling, dictionary-like) ---
# For geometric or ML processing: {net_id: [((x1, y1), (x2, y2)), ...]}
net_segments = {}
for idx, (net, pins) in enumerate(nets.items(), start=1):
    pairs = []
    if len(pins) > 1:
        # Sort pins by X+Y for consistent ordering
        sorted_pins = sorted(pins, key=lambda p: (p["x_mm"], p["y_mm"]))
        for i in range(len(sorted_pins) - 1):
            p1 = sorted_pins[i]
            p2 = sorted_pins[i + 1]
            x1, y1 = int(p1["x_mm"] * 10), int(p1["y_mm"] * 10)
            x2, y2 = int(p2["x_mm"] * 10), int(p2["y_mm"] * 10)
            pairs.append(((x1, y1), (x2, y2)))
    if pairs:
        net_segments[idx] = pairs

txt_path = board.GetFileName().replace(".kicad_pcb", "_net_segments_int.txt")
with open(txt_path, "w") as tf:
    tf.write(str(net_segments))
print(f"💾 Integer TXT saved: {txt_path}\n")

print("🎯 Done! CSV, JSON, and Integer TXT successfully generated.")
