#!/usr/bin/env python3
"""Genera assets/radar.svg — radar de capacidades estilo HUD táctico.

Edita el diccionario CAPACIDADES (valores 0-100) y ejecuta:
    python3 scripts/gen_radar.py
"""
import math
from pathlib import Path

CAPACIDADES = {
    "CIBERSEGURIDAD": 90,
    "GUERRA ELECTRÓNICA": 85,
    "DEVSECOPS": 75,
    "BACKEND": 80,
    "FRONTEND": 65,
    "MÓVIL": 70,
    "SIST. DISTRIBUIDOS": 70,
    "IoT / RF": 60,
}

W, H = 900, 560
CX, CY, R = 450, 295, 190
VERDE, AMBAR, TENUE, FONDO = "#39ff6a", "#f2b84b", "#6f9a66", "#0a0f09"


def punto(i, n, radio):
    ang = -math.pi / 2 + 2 * math.pi * i / n
    return CX + radio * math.cos(ang), CY + radio * math.sin(ang)


def main():
    etiquetas = list(CAPACIDADES)
    n = len(etiquetas)
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Radar de capacidades">')
    p.append("""<defs><style>
.m{font-family:'JetBrains Mono','Fira Code','DejaVu Sans Mono',Consolas,monospace}
.sw{transform-origin:%dpx %dpx;animation:s 5s linear infinite}
@keyframes s{to{transform:rotate(360deg)}}
.area{animation:pu 3s ease-in-out infinite}
@keyframes pu{50%%{fill-opacity:.32}}
</style>
<linearGradient id="bm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s" stop-opacity="0"/><stop offset="1" stop-color="%s" stop-opacity=".45"/></linearGradient>
</defs>""" % (CX, CY, VERDE, VERDE))
    p.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{FONDO}" stroke="#2b4426" stroke-width="2"/>')
    p.append(f'<text x="24" y="34" class="m" font-size="13" fill="{AMBAR}" letter-spacing="3">$ kubectl get capacidades --all-namespaces</text>')
    p.append(f'<text x="{W-24}" y="34" text-anchor="end" class="m" font-size="11" fill="{TENUE}" letter-spacing="2">MODO: RECONOCIMIENTO</text>')

    # anillos y ejes
    for k in range(1, 5):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (punto(i, n, R * k / 4) for i in range(n)))
        p.append(f'<polygon points="{pts}" fill="none" stroke="{VERDE}" stroke-opacity=".22"/>')
    for i in range(n):
        x, y = punto(i, n, R)
        p.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{VERDE}" stroke-opacity=".22"/>')

    # barrido
    x2, y2 = CX + R, CY
    xa, ya = CX + R * math.cos(-math.pi / 4), CY + R * math.sin(-math.pi / 4)
    p.append(f'<g class="sw"><path d="M{CX} {CY}L{x2} {y2}A{R} {R} 0 0 0 {xa:.1f} {ya:.1f}Z" fill="url(#bm)"/>'
             f'<line x1="{CX}" y1="{CY}" x2="{x2}" y2="{y2}" stroke="{VERDE}" stroke-width="1.5"/></g>')

    # área de datos
    datos = [punto(i, n, R * CAPACIDADES[e] / 100) for i, e in enumerate(etiquetas)]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in datos)
    p.append(f'<polygon class="area" points="{pts}" fill="{VERDE}" fill-opacity=".18" stroke="{VERDE}" stroke-width="2"/>')
    for x, y in datos:
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{AMBAR}"/>')

    # etiquetas
    for i, e in enumerate(etiquetas):
        x, y = punto(i, n, R + 26)
        anchor = "middle" if abs(x - CX) < 10 else ("start" if x > CX else "end")
        dy = -4 if y < CY - 10 else (14 if y > CY + 10 else 4)
        p.append(f'<text x="{x:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}" class="m" font-size="12" fill="#e8ffe3">{e} · {CAPACIDADES[e]}</text>')

    p.append(f'<circle cx="{CX}" cy="{CY}" r="3" fill="{VERDE}"/>')
    p.append("</svg>")
    out = Path(__file__).resolve().parent.parent / "assets" / "radar.svg"
    out.write_text("\n".join(p), encoding="utf-8")
    print(f"OK -> {out}")


if __name__ == "__main__":
    main()
