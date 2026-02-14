import pandas as pd
import numpy as np

np.random.seed(42)

# ===== 基本設定 =====
dates = pd.date_range("2026-01-01", "2026-03-31", freq="D")
machines = ["NC-01", "NC-02", "MC-01", "MC-02", "GR-01"]
products = ["丸物A", "角物B", "プレートC"]
shifts = ["昼勤", "夜勤"]

# 原因コード（偏りを作る）
cause_codes = {
    "材料詰まり": 0.35,
    "センサー誤検知": 0.25,
    "位置ズレ": 0.15,
    "作業者リセット": 0.15,
    "原因不明": 0.10
}

rows = []

for date in dates:
    for machine in machines:
        
        # その日の生産数量
        production_qty = np.random.randint(800, 1200)

        # チョコ停発生回数（設備によって偏らせる）
        base_stop = np.random.poisson(lam=8)

        if machine == "NC-02":
            base_stop += np.random.randint(3, 8)  # 問題設備

        for _ in range(base_stop):
            stop_seconds = np.random.randint(10, 180)  # 10秒〜3分
            
            cause = np.random.choice(
                list(cause_codes.keys()),
                p=list(cause_codes.values())
            )

            rows.append([
                date,
                machine,
                np.random.choice(products),
                np.random.choice(shifts),
                production_qty,
                stop_seconds,
                cause
            ])

df = pd.DataFrame(rows, columns=[
    "日付",
    "設備",
    "製品",
    "シフト",
    "生産数量",
    "停止時間(秒)",
    "原因"
])

# ===== 集計列追加 =====
daily_summary = df.groupby(["日付", "設備"]).agg(
    チョコ停回数=("停止時間(秒)", "count"),
    総停止時間=("停止時間(秒)", "sum")
).reset_index()

df = df.merge(daily_summary, on=["日付", "設備"], how="left")

df["停止率(%)"] = (df["総停止時間"] / (8 * 60 * 60)) * 100  # 8時間稼働想定
df["回数/1000個"] = df["チョコ停回数"] / (df["生産数量"] / 1000)

df.to_csv("chocotei_sample_data.csv", index=False, encoding="utf-8-sig")

print("チョコ停サンプルデータを作成しました。")