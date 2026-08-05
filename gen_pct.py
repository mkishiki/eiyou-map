#!/usr/bin/env python3
"""amounts.csv から PCT を生成して app-template.html に埋め込む。

PCT の形: {"栄養素id|食材名": [割合%, 含有量が確認済みか]}
第2要素が 0 の食材は輪郭が点線になる（＝含有量が成分表で未照合）。

v0.5 から、この確認フラグは `含有量の出典` 列を見る。
（v0.4 までは `出典状態` 列で、基準値の話と混ざっていた）
"""
import csv, re, pathlib, sys

HERE = pathlib.Path(__file__).parent
CSV  = HERE / "amounts.csv"
TPL  = HERE / "src" / "app-template.html"

rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))

if "含有量の出典" not in rows[0]:
    sys.exit("含有量の出典 列がありません。列分離が済んでいない csv です")

items = []
for r in rows:
    key  = f'{r["栄養素id"]}|{r["食材"]}'
    pct  = float(r["割合%"])
    conf = 1 if r["含有量の出典"].strip() == "確認済" else 0
    pct_s = str(int(pct)) + ".0" if pct == int(pct) else str(pct)
    items.append(f'"{key}":[{pct_s},{conf}]')

pct_js = "const PCT={" + ",".join(items) + "};"

tpl = TPL.read_text(encoding="utf-8")
new, n = re.subn(r"^const PCT=\{.*?\};$", lambda m: pct_js, tpl,
                 count=1, flags=re.M | re.S)
if n != 1:
    sys.exit("テンプレート内の const PCT={...}; が見つかりません")

TPL.write_text(new, encoding="utf-8")

conf_n = sum(1 for r in rows if r["含有量の出典"].strip() == "確認済")
print(f"PCT を更新: {len(items)}件  ({len(pct_js):,} chars)")
print(f"  実線（含有量 確認済）: {conf_n}件")
print(f"  点線（含有量 未確認）: {len(items)-conf_n}件")
