# 🧩 KiCad Net Extractor — CSV, JSON & Integer TXT Export

**KiCad Net Extractor** is a lightweight Python script designed to run directly inside **KiCad’s PCB Editor (Pcbnew)** via the **Scripting Console**.
It extracts a clean, grouped netlist from any `.kicad_pcb` board file — including each component, pin, and absolute coordinate — and exports it in multiple formats ready for analysis, routing, or dataset generation.

---

## ⚡️ Features

* ✅ Works inside **KiCad 6, 7, and 8** (using the built-in `pcbnew` module)
* 📊 Exports three synchronized output files:

  * **CSV** → easy to open in Excel, Pandas, or MATLAB
  * **JSON** → grouped by net, perfect for automation and AI pipelines
  * **TXT** → integer-scaled dictionary (for geometric routing or ML datasets)
* 🧭 Includes **layer (Front/Back)** and **component-pin mapping**
* ⚙️ Automatically converts floating coordinates to **integers ×10** for compact datasets
* 💡 Robust against KiCad API version changes (safe parent reference handling)

---

## 📂 Output Example

### **1️⃣ CSV (`board_netlist_grouped.csv`)**

```
Net,Component,Pin,X(mm),Y(mm),Side
GND,U1,1,100.25,75.48,Front
GND,U2,2,125.78,76.03,Front
+5V,U3,3,120.00,70.20,Front
```

### **2️⃣ JSON (`board_netlist_grouped.json`)**

```json
{
  "GND": [
    {"component": "U1", "pin": "1", "x_mm": 100.25, "y_mm": 75.48, "side": "Front"},
    {"component": "U2", "pin": "2", "x_mm": 125.78, "y_mm": 76.03, "side": "Front"}
  ],
  "+5V": [
    {"component": "U3", "pin": "3", "x_mm": 120.00, "y_mm": 70.20, "side": "Front"}
  ]
}
```

### **3️⃣ Integer TXT (`board_net_segments_int.txt`)**

```
{
  1: [((942, 501), (944, 557))],
  2: [((930, 513), (944, 562)), ((944, 562), (810, 498))],
  3: [((914, 547), (857, 511))]
}
```

---

## 🧠 How It Works

1. Uses the **KiCad `pcbnew` API** to iterate through every pad on the board.
2. Groups pads by their **net name**.
3. Extracts:

   * Component reference (`U1`, `R5`, etc.)
   * Pin number
   * Absolute X/Y position in millimeters
   * Board side (Front or Back)
4. Exports:

   * A full **grouped netlist** (CSV & JSON)
   * A simplified **integer-based topology file** for numerical or routing tasks

---

## 🚀 How to Use

### **1️⃣ Open KiCad PCB Editor**

Open your `.kicad_pcb` file in **Pcbnew**.

### **2️⃣ Open the Scripting Console**

Menu → **Tools → Scripting Console**

### **3️⃣ Run the Script**

Save the script as:

```
net_extractor.py
```

Then in the console, run:

```python
exec(open("net_extractor.py").read())
```

You’ll see a grouped summary printed, and three files generated in your project directory.

---

## 🧾 Output Files Summary

| File                     | Type | Description                                       |
| ------------------------ | ---- | ------------------------------------------------- |
| `*_netlist_grouped.csv`  | CSV  | Component, pin, X/Y, and layer (Front/Back)       |
| `*_netlist_grouped.json` | JSON | Hierarchical netlist grouped by net               |
| `*_net_segments_int.txt` | TXT  | Integer-scaled net dictionary for algorithmic use |

---

## 🧰 Requirements

* **KiCad 6.0 or newer**
* Runs inside **Pcbnew’s Scripting Console**
* No external dependencies required (uses built-in Python + `pcbnew`)

---

## 🧑‍💻 Example Applications

* Routing algorithm testing (ACO, DRL, PSO, etc.)
* Geometric PCB dataset generation (PCBench, GPCB, etc.)
* Connectivity visualization / DRC analysis
* Machine learning feature extraction from real boards

---

## ⚙️ Customization Ideas

You can easily extend the script to include:

* Component **rotation** and **footprint name**
* Via / trace extraction
* Multi-layer segment detection
* Export in **NPZ**, **GeoJSON**, or **Pickle** for ML pipelines

---

## 📜 License

This project is released under the **MIT License** — feel free to modify and integrate into your own research, routing tools, or datasets.

---

## 🧩 Acknowledgments

This script is designed for fast, precise, and human-readable PCB data extraction —
ideal for research, AI, and automation projects.

If you want to build automated AI-assisted routing tools, dataset converters, or visualization dashboards, this extractor is the foundation.

---

Would you like me to add a **section with a diagram** (showing “Board → Pads → Nets → CSV/JSON/TXT pipeline”) for the README? It makes the GitHub page look more professional and instantly understandable.

