import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="真戦テンプレ編成検索",
    layout="wide"
)

st.title("⚔️ 信長の野望 真戦 テンプレ編成検索")

@st.cache_data
def load_data():
    return pd.read_csv("formations.csv")

df = load_data()

# サイドバー
st.sidebar.header("検索条件")

season = st.sidebar.selectbox(
    "シーズン",
    ["ALL"] + sorted(df["season"].unique().tolist())
)

tier = st.sidebar.selectbox(
    "Tier",
    ["ALL"] + sorted(df["tier"].unique().tolist())
)

keyword = st.sidebar.text_input("武将・戦法キーワード")

# フィルタ
filtered_df = df.copy()

if season != "ALL":
    filtered_df = filtered_df[
        filtered_df["season"] == season
    ]

if tier != "ALL":
    filtered_df = filtered_df[
        filtered_df["tier"] == tier
    ]

if keyword:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: keyword.lower() in str(row).lower(),
            axis=1
        )
    ]

st.subheader(f"検索結果：{len(filtered_df)}件")

for _, row in filtered_df.iterrows():

    with st.container(border=True):

        st.markdown(f"## {row['formation_name']}")

        col1, col2, col3 = st.columns(3)

        col1.metric("Season", row["season"])
        col2.metric("Tier", row["tier"])
        col3.metric("兵種", row["troop_type"])

        st.write(f"### 主将")
        st.write(row["leader"])

        st.write(f"### 副将")
        st.write(f"{row['sub1']} / {row['sub2']}")

        st.write("### 戦法")
        st.write(row["skills"])

        st.write("### 特徴")
        st.write(row["description"])

st.divider()

st.caption("created with Streamlit")
