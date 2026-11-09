import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Indian Election Dashboard", layout="wide")
st.markdown(
"""
<style>
.tricolour-strip {
position: fixed;
left: 0;
width: 100vw;
height: 18px;
z-index: 1000002;
pointer-events: none;
display: flex;
flex-direction: column;
box-shadow: 0 0 2px rgba(0, 0, 0, 0.35);
}
.tricolour-strip.top { top: 0; }
.tricolour-strip.bottom { bottom: 0; }
.tricolour-strip span {
display: block;
flex: 1 1 0;
width: 100%;
}
.tricolour-strip .saffron { background: #FF9933; }
.tricolour-strip .white { background: #FFFFFF; }
.tricolour-strip .green { background: #138808; }

header[data-testid="stHeader"] { top: 18px; }
.block-container { padding-bottom: 4rem; }
[data-testid="stSidebar"] > div:first-child { padding-top: 18px; padding-bottom: 24px; }

html, body, .stApp,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp p, .stApp li, .stApp label, .stApp button, .stApp input, .stApp textarea,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stAlert"],
.stApp [data-baseweb="select"],
.stApp [data-baseweb="tab"],
.stApp [data-baseweb="tag"],
.stApp [data-testid="stWidgetLabel"] {
font-family: Arial, "Helvetica Neue", Helvetica, sans-serif !important;
}

.stApp h1 { font-size: 2.1rem !important; font-weight: 700 !important; }
.stApp h2 { font-size: 1.6rem !important; font-weight: 700 !important; }
.stApp h3 { font-size: 1.25rem !important; font-weight: 700 !important; }
.stApp p, .stApp li { font-size: 1rem; }
.stApp label, .stApp [data-testid="stWidgetLabel"] p { font-size: 0.9rem !important; }
.stApp [data-baseweb="tab"] p { font-size: 1rem !important; }
.stApp [data-testid="stMetricLabel"] p { font-size: 0.9rem !important; }
.stApp [data-testid="stMetricValue"] { font-size: 1.6rem !important; }
.stApp [data-testid="stCaptionContainer"] p { font-size: 0.85rem !important; }

section.main h1::before,
[data-testid="stMain"] h1::before {
content: "";
display: inline-block;
width: 44px;
height: 30px;
margin-right: 14px;
vertical-align: middle;
background-repeat: no-repeat;
background-size: 100% 100%;
background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 24'><rect width='36' height='8' fill='%23FF9933'/><rect y='8' width='36' height='8' fill='%23FFFFFF'/><rect y='16' width='36' height='8' fill='%23138808'/><g stroke='%23000080' stroke-width='0.5' fill='none'><circle cx='18' cy='12' r='3.2'/><line x1='18' y1='8.8' x2='18' y2='15.2'/><line x1='14.8' y1='12' x2='21.2' y2='12'/><line x1='15.74' y1='9.74' x2='20.26' y2='14.26'/><line x1='15.74' y1='14.26' x2='20.26' y2='9.74'/></g><rect x='0.25' y='0.25' width='35.5' height='23.5' fill='none' stroke='%23999999' stroke-width='0.3'/></svg>");
}
</style>
<div class="tricolour-strip top"><span class="saffron"></span><span class="white"></span><span class="green"></span></div>
<div class="tricolour-strip bottom"><span class="saffron"></span><span class="white"></span><span class="green"></span></div>
""",
    unsafe_allow_html=True
)

data = pd.read_csv("indian-state-level-election.csv")

st.title("Indian State-Level Election Dashboard")
st.write("Analysis of election records, candidates, political parties and voting patterns.")

st.sidebar.title("Filters")

states = sorted(data["st_name"].dropna().unique())

selected_states = st.sidebar.multiselect(
    "Select States",
    states,
    default=states
)

years = sorted(data["year"].dropna().unique())

selected_years = st.sidebar.select_slider(
    "Select Election Year Range",
    options=years,
    value=(years[0], years[-1])
)

parties = ["All Parties"] + sorted(data["partyname"].dropna().unique())

selected_party = st.sidebar.selectbox(
    "Select Political Party",
    parties
)

genders = sorted(data["cand_sex"].dropna().unique())
selected_gender = st.sidebar.multiselect(
    "Select Candidate Gender",
    genders,
    default=genders
)

filtered_data = data[
    (data["st_name"].isin(selected_states)) &
    (data["year"] >= selected_years[0]) &
    (data["year"] <= selected_years[1]) &
    (data["cand_sex"].isin(selected_gender))
]

if selected_party != "All Parties":
    filtered_data = filtered_data[
        filtered_data["partyname"] == selected_party
    ]

st.sidebar.write("Filtered Records:", len(filtered_data))

#Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard Overview",
    "Data Analysis",
    "Visualizations",
    "Insights"
])

#OVERVIEW
with tab1:

    st.header("Election Overview")

    if len(filtered_data) > 0:

        with st.container():
            total_records = len(filtered_data)
            total_votes = filtered_data["totvotpoll"].sum()
            average_votes = filtered_data["totvotpoll"].mean()
            total_states = filtered_data["st_name"].nunique()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Records", f"{total_records:,}")
            col2.metric("Total Votes", f"{total_votes:,.0f}")
            col3.metric("Average Votes", f"{average_votes:,.2f}")
            col4.metric("States / UTs", total_states)

        st.subheader("State-wise Record Count")
        state_count = filtered_data.groupby("st_name").size().reset_index(name="Records")
        st.dataframe(state_count, use_container_width=True)
        with st.expander("View Complete Dataset"):
            st.dataframe(filtered_data, use_container_width=True)

    else:
        st.warning("No records found. Please change the filters.")

#DATA ANALYSIS
with tab2:

    st.header("Data Analysis")

    if len(filtered_data) > 0:
        st.subheader("Summary Statistics")
        st.write(
            filtered_data[["year", "totvotpoll", "electors"]].describe()
        )

        st.subheader("Party-wise Candidate Count")
        party_count = filtered_data.groupby("partyname").size().reset_index(name="Candidates")

        st.dataframe(
            party_count.sort_values("Candidates", ascending=False).head(15),
            use_container_width=True
        )
        st.subheader("Gender-wise Candidate Count")

        gender_count = filtered_data.groupby("cand_sex").size().reset_index(name="Candidates")
        st.dataframe(gender_count, use_container_width=True)
        st.subheader("Missing Values")
        missing = filtered_data.isnull().sum()
        st.dataframe(
            missing.reset_index().rename(
                columns={"index": "Column", 0: "Missing Values"}
            ),
            use_container_width=True
        )

    else:
        st.warning("No records available.")

#VISUALIZATION
with tab3:

    st.header("Election Visualizations")

    if len(filtered_data) > 0:

        st.subheader("1. State-wise Total Votes")
        state_votes = filtered_data.groupby("st_name")["totvotpoll"].sum().sort_values(ascending=False).head(10)
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.bar(state_votes.index, state_votes.values)
        ax1.set_title("Top 10 States by Total Votes")
        ax1.set_xlabel("States")
        ax1.set_ylabel("Total Votes")
        ax1.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)
        st.write("Interpretation: This bar chart compares the total candidate votes recorded across the top 10 states.")

        st.subheader("2. Year-wise Voting Trend")
        year_votes = filtered_data.groupby("year")["totvotpoll"].sum().sort_index()

        fig2, ax2 = plt.subplots(figsize=(10, 5))

        ax2.plot(year_votes.index, year_votes.values, marker="o")
        ax2.set_title("Year-wise Total Votes")
        ax2.set_xlabel("Election Year")
        ax2.set_ylabel("Total Votes")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)
        st.write("Interpretation: This line chart shows the variation in total candidate votes across different election years.")


        st.subheader("3. Electors vs Total Votes")
        constituency_data = filtered_data.groupby(
            ["st_name", "year", "ac_no", "ac_name"],
            dropna=False
        ).agg(
            total_votes=("totvotpoll", "sum"),
            electors=("electors", "first")
        ).reset_index()

        fig3, ax3 = plt.subplots(figsize=(10, 5))

        ax3.scatter(
            constituency_data["electors"],
            constituency_data["total_votes"],
            alpha=0.5
        )

        ax3.set_title("Electors vs Total Candidate Votes")
        ax3.set_xlabel("Number of Electors")
        ax3.set_ylabel("Total Candidate Votes")

        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)
        st.write("Interpretation: This scatter plot helps examine the relationship between the number of electors and the total candidate votes in each constituency.")
    else:
        st.warning("No records available for visualization.")

with tab4:

    st.header("Key Election Insights")

    if len(filtered_data) > 0:
        top_state = filtered_data.groupby("st_name")["totvotpoll"].sum().idxmax()
        top_party = filtered_data.groupby("partyname").size().idxmax()
        top_year = filtered_data.groupby("year")["totvotpoll"].sum().idxmax()
        female_count = len(filtered_data[filtered_data["cand_sex"] == "F"])
        st.subheader("Important Observations")
        st.write("1. State with the highest total candidate votes:", top_state)
        st.write("2. Party with the highest number of candidate records:", top_party)
        st.write("3. Year with the highest total candidate votes:", top_year)
        st.write("4. Number of female candidate records:", female_count)
        st.write("5. Total records after applying filters:", len(filtered_data))

    else:
        st.warning("No insights available.")

st.divider()
st.caption("Indian State-Level Election Analysis | Developed using Python, Pandas, Matplotlib and Streamlit")