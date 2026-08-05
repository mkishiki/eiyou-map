#!/usr/bin/env python3
"""tabeawase-data.js と app-template.html を束ねて、配布用の1ファイルHTMLを作る。
   使い方:  python3 src/build.py
   出力:    eiyou-map.html
"""
import pathlib, sys

here = pathlib.Path(__file__).parent
out  = here.parent / "eiyou-map.html"

data = (here / "tabeawase-data.js").read_text(encoding="utf-8")
tpl  = (here / "app-template.html").read_text(encoding="utf-8")

if "/*__DATA__*/" not in tpl:
    sys.exit("テンプレートに /*__DATA__*/ が見つかりません")

html = tpl.replace("/*__DATA__*/", data.rstrip() + "\n")
out.write_text(html, encoding="utf-8")
print(f"built: {out}  ({len(html):,} chars / data {len(data):,} chars)")
