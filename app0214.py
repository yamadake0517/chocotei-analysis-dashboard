import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["font.family"] = "Meiryo"

st.set_page_config(page_title="チョコ停分析ダッシュボード", layout="wide")

st.title("チョコ停分析ダッシュボード")

uploaded_file = st.file_uploader("chocotei_sample_data.csv をアップロード", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["日付"])

    # ===== サイドバー =====
    st.sidebar.header("分析条件")

    selected_machine = st.sidebar.multiselect(
        "設備選択",
        df["設備"].unique(),
        default=df["設備"].unique()
    )

    selected_month = st.sidebar.multiselect(
        "月選択",
        df["日付"].dt.to_period("M").astype(str).unique(),
        default=df["日付"].dt.to_period("M").astype(str).unique()
    )

    df = df[df["設備"].isin(selected_machine)]
    df = df[df["日付"].dt.to_period("M").astype(str).isin(selected_month)]

    # ===== KPI =====
    st.subheader("KPIサマリ")

    total_stops = df["チョコ停回数"].sum()
    total_stop_time = df["総停止時間"].sum()
    avg_rate = df["停止率(%)"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("総チョコ停回数", int(total_stops))
    col2.metric("総停止時間(秒)", int(total_stop_time))
    col3.metric("平均停止率(%)", round(avg_rate, 2))

    # ===== 設備別ランキング =====
    st.subheader("設備別 チョコ停回数")

    machine_summary = df.groupby("設備")["チョコ停回数"].sum().sort_values(ascending=False)
    st.bar_chart(machine_summary)

    # ===== 原因パレート図 =====
    st.subheader("原因パレート図")

    cause_summary = df["原因"].value_counts().sort_values(ascending=False)

    fig, ax = plt.subplots()
    cause_summary.plot(kind="bar", ax=ax)
    ax.set_ylabel("発生回数")
    st.pyplot(fig)

    # ===== 月別推移 =====
    st.subheader("月別 チョコ停回数推移")

    monthly = df.groupby(df["日付"].dt.to_period("M"))["チョコ停回数"].sum()
    st.line_chart(monthly)

    # ===== シフト比較 =====
    st.subheader("シフト別 チョコ停回数")

    shift_summary = df.groupby("シフト")["チョコ停回数"].sum()
    st.bar_chart(shift_summary)

    # ===== 生産数量あたり比較 =====
    st.subheader("回数 / 1000個 比較")

    rate_summary = df.groupby("設備")["回数/1000個"].mean().sort_values(ascending=False)
    st.bar_chart(rate_summary)

    st.success("分析完了。改善優先順位を確認してください。")
    # ===== 原因 × 設備 ヒートマップ =====
    st.subheader("原因 × 設備 ヒートマップ")

    heatmap_data = df.groupby(["原因", "設備"]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 5))
    cax = ax.imshow(heatmap_data, aspect='auto')

    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_yticks(range(len(heatmap_data.index)))

    ax.set_xticklabels(heatmap_data.columns)
    ax.set_yticklabels(heatmap_data.index)

    plt.colorbar(cax)

    st.pyplot(fig)