#!/usr/bin/env python3
"""Cıvata çiziminin vurgulu sürümlerini üretir: assets/civata-vurgu-<mod>.svg
Modlar: cap (M8), adim (1,25), boy (40 mm), sinif (8.8 baş işareti)."""
import os

ACC, W = "#FFC629", "#FFFFFF"


def svg(mode):
    def c(part):  # (renk, saydamlık)
        return (ACC, 1) if part == mode else (W, 0.28)

    hx, hxo = c("sinif")
    ln, lno = c("boy")
    dm, dmo = c("cap")
    pt, pto = c("adim")
    threads = "".join('<line x1="%d" y1="112" x2="%d" y2="188"></line>' % (x, x + 10) for x in range(568, 825, 16))
    return f'''<svg width="968" height="300" viewBox="0 0 968 300" aria-hidden="true" style="display:block">
<g stroke="{hx}" stroke-opacity="{hxo}" fill="none" stroke-width="4" stroke-linejoin="round"><polygon points="170,150 133,86 59,86 22,150 59,214 133,214"></polygon></g>
<text x="96" y="165" text-anchor="middle" font-family="Barlow Condensed, Arial Narrow, sans-serif" font-weight="700" font-size="44" fill="{hx}" fill-opacity="{max(hxo, 0.5)}">8.8</text>
<line x1="178" y1="150" x2="244" y2="150" stroke="#C7D3E6" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="6 8"></line>
<g stroke="#FFFFFF" fill="none" stroke-linejoin="round">
<rect x="250" y="72" width="96" height="156" stroke-width="4"></rect>
<line x1="250" y1="124" x2="346" y2="124" stroke-width="2.5"></line><line x1="250" y1="176" x2="346" y2="176" stroke-width="2.5"></line>
<path d="M346 112 H840 L852 124 V176 L840 188 H346 Z" stroke-width="4"></path>
<line x1="560" y1="112" x2="560" y2="188" stroke-width="2"></line>
<line x1="560" y1="120" x2="840" y2="120" stroke-width="1.5" stroke-opacity="0.55"></line><line x1="560" y1="180" x2="840" y2="180" stroke-width="1.5" stroke-opacity="0.55"></line>
</g>
<g stroke="{pt if mode == 'adim' else W}" stroke-width="{3 if mode == 'adim' else 2.5}">{threads}</g>
<g stroke="{ln}" stroke-opacity="{lno}" fill="{ln}" fill-opacity="{lno}">
<line x1="346" y1="196" x2="346" y2="272" stroke-width="2"></line><line x1="852" y1="184" x2="852" y2="272" stroke-width="2"></line>
<line x1="360" y1="258" x2="838" y2="258" stroke-width="3"></line>
<polygon points="346,258 364,249 364,267" stroke="none"></polygon><polygon points="852,258 834,249 834,267" stroke="none"></polygon>
<text x="599" y="242" text-anchor="middle" font-family="Barlow Condensed, Arial Narrow, sans-serif" font-weight="700" font-size="34" stroke="none">40 mm</text>
</g>
<g stroke="{dm}" stroke-opacity="{dmo}" fill="{dm}" fill-opacity="{dmo}">
<line x1="860" y1="112" x2="934" y2="112" stroke-width="2"></line><line x1="860" y1="188" x2="934" y2="188" stroke-width="2"></line>
<line x1="914" y1="126" x2="914" y2="174" stroke-width="3"></line>
<polygon points="914,112 905,130 923,130" stroke="none"></polygon><polygon points="914,188 905,170 923,170" stroke="none"></polygon>
<text x="914" y="96" text-anchor="middle" font-family="Barlow Condensed, Arial Narrow, sans-serif" font-weight="700" font-size="34" stroke="none">M8</text>
</g>
<g stroke="{pt}" stroke-opacity="{pto}" fill="{pt}" fill-opacity="{pto}">
<line x1="744" y1="106" x2="744" y2="68" stroke-width="2"></line><line x1="760" y1="106" x2="760" y2="68" stroke-width="2"></line>
<line x1="744" y1="76" x2="760" y2="76" stroke-width="2"></line>
<text x="752" y="56" text-anchor="middle" font-family="Barlow Condensed, Arial Narrow, sans-serif" font-weight="700" font-size="30" stroke="none">1,25</text>
</g>
</svg>
'''


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    for m in ("cap", "adim", "boy", "sinif"):
        with open(os.path.join(root, "assets", "civata-vurgu-%s.svg" % m), "w", encoding="utf-8") as f:
            f.write(svg(m))
        print("ok", m)
