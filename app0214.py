import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="チョコ停分析ダッシュボード", layout="wide")
st.title("チョコ停分析ダッシュボード")

# 日本語フォント対応
import matplotlib
matplotlib.rcParams["font.family"] = "Meiryo"

# サンプルデータ読み込み
@st.cache_data
def load_sample_data():
    return pd.read_csv("sample_data/chocotei_sample_data.csv", parse_dates=["日付"])
df = load_sample_data()

# サイドバー条件
selected_machine = st.sidebar.multiselect(
    "設備選択", df["設備"].unique(), default=df["設備"].unique()
)
selected_month = st.sidebar.multiselect(
    "月選択", df["日付"].dt.to_period("M").astype(str).unique(),
    default=df["日付"].dt.to_period("M").astype(str).unique()
)
df = df[df["設備"].isin(selected_machine)]
df = df[df["日付"].dt.to_period("M").astype(str).isin(selected_month)]

# ===== KPIカード（背景色付き） =====
st.subheader("KPIサマリ")
total_stops = df["チョコ停回数"].sum()
total_stop_time = df["総停止時間"].sum()
avg_rate = df["停止率(%)"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("総チョコ停回数", int(total_stops))
col2.metric("総停止時間(秒)", int(total_stop_time))
col3.metric("平均停止率(%)", round(avg_rate, 2))

# ===== 設備別ランキング & 原因パレート（折りたたみカード） =====
st.subheader("ランキング・原因分析")
with st.expander("設備別 チョコ停回数（タップで展開）", expanded=True):
    machine_summary = df.groupby("設備")["チョコ停回数"].sum().sort_values(ascending=False)
    st.bar_chart(machine_summary, use_container_width=True)

with st.expander("原因パレート図（タップで展開）", expanded=True):
    cause_summary = df["原因"].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots()
    cause_summary.plot(kind="bar", ax=ax)
    ax.set_ylabel("発生回数")
    st.pyplot(fig)

# ===== 月別推移 & シフト比較（折りたたみカード） =====
st.subheader("推移・シフト分析")
with st.expander("月別 チョコ停回数推移", expanded=True):
    monthly = df.groupby(df["日付"].dt.to_period("M"))["チョコ停回数"].sum()
    st.line_chart(monthly, use_container_width=True)

with st.expander("シフト別 チョコ停回数", expanded=True):
    shift_summary = df.groupby("シフト")["チョコ停回数"].sum()
    st.bar_chart(shift_summary, use_container_width=True)

# ===== ヒートマップ & 回数/1000個 =====
st.subheader("詳細分析")
with st.expander("原因×設備ヒートマップ", expanded=True):
    heatmap_data = df.groupby(["原因", "設備"]).size().unstack(fill_value=0)
    st.dataframe(heatmap_data.style.background_gradient(cmap="Reds"))

with st.expander("回数 / 1000個 比較", expanded=True):
    rate_summary = df.groupby("設備")["回数/1000個"].mean().sort_values(ascending=False)
    st.bar_chart(rate_summary, use_container_width=True)

st.success("カード型UI＋折りたたみでポートフォリオ感アップ！")