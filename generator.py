from __future__ import annotations

import json
import math
import re
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent


def _integer(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or int(value) != value:
        raise ValueError(f"{name} precisa ser um número inteiro.")
    result = int(value)
    if not low <= result <= high:
        raise ValueError(f"{name} deve ficar entre {low} e {high}.")
    return result


def build_layout(config: dict) -> dict:
    """Builds a fictional panel layout from a small, explicit configuration."""
    if not isinstance(config, dict):
        raise ValueError("A configuração deve ser um objeto JSON.")
    width = _integer(config.get("width_mm", 900), "Largura", 600, 1600)
    height = _integer(config.get("height_mm", 1600), "Altura", 1000, 2400)
    drive_count = _integer(config.get("drive_count", 2), "Módulos de acionamento", 0, 8)
    control_count = _integer(config.get("control_count", 1), "Módulos de controle", 1, 5)
    terminal_count = _integer(config.get("terminal_count", 12), "Bornes demonstrativos", 4, 48)
    title = str(config.get("title", "Painel didático sintético"))[:80]

    margin = 65
    gap = 22
    drive_w, drive_h = 142, 208
    drive_capacity = max(1, (width - 2 * margin + gap) // (drive_w + gap))
    if drive_count > drive_capacity * 2:
        raise ValueError(f"A largura escolhida comporta até {drive_capacity * 2} módulos de acionamento neste estudo.")
    components = []
    def add(cid, kind, label, x, y, w, h):
        components.append({"id": cid, "kind": kind, "label": label, "x": int(x), "y": int(y), "w": int(w), "h": int(h)})

    # Upper control row: one protection block followed by fictional controller modules.
    add("P-01", "protection", "Proteção demonstrativa", margin, 105, 115, 120)
    control_w, control_h = 116, 120
    for i in range(control_count):
        x = margin + 145 + i * (control_w + 18)
        if x + control_w > width - margin:
            raise ValueError("Reduza os módulos de controle ou aumente a largura do painel.")
        add(f"C-{i+1:02d}", "control", f"Controle {i+1}", x, 105, control_w, control_h)

    # Drives are distributed over one or two rails using the same coordinate model used by both views.
    for i in range(drive_count):
        row, col = divmod(i, drive_capacity)
        y = 390 + row * 275
        x = margin + col * (drive_w + gap)
        if y + drive_h > height - 190:
            raise ValueError("A altura escolhida não deixa espaço para os módulos e bornes. Aumente a altura do painel.")
        add(f"A-{i+1:02d}", "drive", f"Acionamento {i+1}", x, y, drive_w, drive_h)

    terminal_w = max(150, min(width - 2 * margin, terminal_count * 18 + 22))
    add("T-01", "terminals", f"Bornes demonstrativos · {terminal_count} posições", margin, height - 145, terminal_w, 68)

    rails = [120, 270]
    rails.extend(sorted({c["y"] - 14 for c in components if c["kind"] == "drive"}))
    rails = sorted(set(y for y in rails if 80 < y < height - 170))
    # Basic bounds check. Labels and symbols stay inside the plate area.
    for c in components:
        if c["x"] < margin or c["y"] < 75 or c["x"] + c["w"] > width - margin or c["y"] + c["h"] > height - 70:
            raise ValueError(f"{c['id']} ultrapassa a área útil demonstrativa.")
    return {
        "project": {"name": title, "revision": "A", "classification": "DEMONSTRAÇÃO · DADOS FICTÍCIOS"},
        "enclosure": {"width_mm": width, "height_mm": height, "depth_mm": 300, "margin_mm": margin},
        "counts": {"drives": drive_count, "controls": control_count, "terminal_positions": terminal_count},
        "rails_y": rails,
        "components": components,
        "limitations": [
            "Geometria didática; dimensões e módulos são inventados.",
            "Não dimensiona circuito, proteção, ventilação ou segurança.",
            "Não liberar para fabricação ou instalação."
        ]
    }


def layout_svg(layout: dict) -> str:
    w, h = layout["enclosure"]["width_mm"], layout["enclosure"]["height_mm"]
    palette = {"protection": ("#82652f", "#f0cc7a"), "control": ("#315b71", "#8ed3ee"), "drive": ("#335d9b", "#a9c7ff"), "terminals": ("#2c6a59", "#9ce6c8")}
    scale = min(760 / w, 560 / h)
    sw, sh = w * scale, h * scale
    ox, oy = (900 - sw) / 2, 52
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 680" role="img" aria-label="Arranjo 2D sintético">',
             '<defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#213247" stroke-width=".7"/></pattern></defs>',
             '<rect width="900" height="680" fill="#0b1420"/><rect width="900" height="680" fill="url(#g)"/>',
             '<text x="32" y="32" fill="#7d94aa" font-size="11" font-family="monospace">VISTA INTERNA · LAYOUT SINTÉTICO</text>',
             f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{sw:.1f}" height="{sh:.1f}" rx="7" fill="#142334" stroke="#92a8b9" stroke-width="2"/>',
             f'<rect x="{ox+10:.1f}" y="{oy+10:.1f}" width="{sw-20:.1f}" height="{sh-20:.1f}" rx="3" fill="#0c1723" stroke="#34495d"/>']
    for y in layout["rails_y"]:
        yy = oy + y * scale
        parts.append(f'<rect x="{ox+18:.1f}" y="{yy:.1f}" width="{sw-36:.1f}" height="5" rx="2" fill="#607a8f" opacity=".72"/>')
    for c in layout["components"]:
        fill, stroke = palette[c["kind"]]
        x, y, cw, ch = ox+c["x"]*scale, oy+c["y"]*scale, c["w"]*scale, c["h"]*scale
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="5" fill="{fill}" fill-opacity=".8" stroke="{stroke}" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+5:.1f}" y="{y+16:.1f}" fill="#f4f7fb" font-size="{max(8,min(12,scale*12)):.1f}" font-family="sans-serif">{c["id"]}</text>')
        if c["kind"] == "drive":
            parts.append(f'<circle cx="{x+cw/2:.1f}" cy="{y+ch*.45:.1f}" r="{max(5,min(14,cw*.18)):.1f}" fill="#0c1b31" stroke="#b9d0f7"/>')
            parts.append(f'<path d="M{x+cw*.2:.1f} {y+ch*.72:.1f}h{cw*.6:.1f}" stroke="#c5d5e4" stroke-width="2"/>')
    parts.append(f'<text x="{ox:.1f}" y="{oy+sh+24:.1f}" fill="#94a9bb" font-size="10" font-family="monospace">{w} × {h} mm · unidades fictícias</text>')
    parts.append('<text x="32" y="651" fill="#65dcb8" font-size="10" font-family="monospace">DADOS FICTÍCIOS · SEM ESCALA DE FABRICAÇÃO</text></svg>')
    return "".join(parts)


def dxf_text(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9 ._:/+-]", "", text)
    return text[:70]


def layout_dxf(layout: dict) -> str:
    """Write a minimal ASCII DXF R12 with panel outline, rails, and component rectangles."""
    w, h = layout["enclosure"]["width_mm"], layout["enclosure"]["height_mm"]
    entities = []
    def line(x1, y1, x2, y2, layer="GEOMETRY"):
        entities.extend(["0", "LINE", "8", layer, "10", f"{x1:.3f}", "20", f"{h-y1:.3f}", "30", "0", "11", f"{x2:.3f}", "21", f"{h-y2:.3f}", "31", "0"])
    def rect(x, y, rw, rh, layer):
        line(x,y,x+rw,y,layer); line(x+rw,y,x+rw,y+rh,layer); line(x+rw,y+rh,x,y+rh,layer); line(x,y+rh,x,y,layer)
    def text(x,y,value,size=18,layer="LABEL"):
        entities.extend(["0","TEXT","8",layer,"10",f"{x:.3f}","20",f"{h-y:.3f}","30","0","40",f"{size:.3f}","1",dxf_text(value)])
    rect(0,0,w,h,"ENCLOSURE")
    rect(18,18,w-36,h-36,"PLATE")
    for i,y in enumerate(layout["rails_y"],1):
        line(40,y,w-40,y,f"RAIL_{i}")
    for c in layout["components"]:
        rect(c["x"],c["y"],c["w"],c["h"],c["kind"].upper())
        text(c["x"]+5,c["y"]+22,c["id"],18,"LABEL")
    text(35,35,"SYNTHETIC PANEL LAYOUT - DEMO ONLY",24,"NOTICE")
    return "\n".join(["0","SECTION","2","HEADER","9","$ACADVER","1","AC1009","0","ENDSEC","0","SECTION","2","TABLES","0","TABLE","2","LAYER","70","6"]+
        sum((["0","LAYER","2",name,"70","0","62",str(color),"6","CONTINUOUS"] for name,color in [("0",7),("ENCLOSURE",8),("PLATE",7),("GEOMETRY",7),("LABEL",3),("NOTICE",1),("PROTECTION",2),("CONTROL",4),("DRIVE",5),("TERMINALS",3)]),[])+
        ["0","ENDTAB","0","ENDSEC","0","SECTION","2","ENTITIES"]+entities+["0","ENDSEC","0","EOF",""])


def generate(config: dict, out_dir: Path | None = None) -> dict:
    layout = build_layout(config)
    svg = layout_svg(layout)
    dxf = layout_dxf(layout)
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "panel_config.json").write_text(json.dumps(layout, ensure_ascii=False, indent=2), encoding="utf-8")
        (out_dir / "panel_layout.svg").write_text(svg, encoding="utf-8")
        (out_dir / "panel_layout.dxf").write_text(dxf, encoding="ascii")
    return {"layout": layout, "svg": svg, "dxf_bytes": len(dxf.encode("ascii")), "summary": f"{len(layout['components'])} blocos sintéticos · {layout['enclosure']['width_mm']} × {layout['enclosure']['height_mm']} mm"}


if __name__ == "__main__":
    sample = {"width_mm": 900, "height_mm": 1600, "drive_count": 2, "control_count": 1, "terminal_count": 12}
    result = generate(sample, APP_DIR / "outputs")
    print(result["summary"])

