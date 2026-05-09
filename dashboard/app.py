import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Steam Game Success Dashboard", layout="wide")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "dashboard_data.csv"
CLEANED_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "cleaned_games.csv"


def parse_list_string(value):
    if pd.isna(value):
        return []
    text = str(value).strip()
    if text.startswith('[') and text.endswith(']'):
        text = text[1:-1]
    items = [item.strip().strip("'\"") for item in text.split(',') if item.strip()]
    return items


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['Release date'] = pd.to_datetime(df['Release date'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['owners_mid'] = pd.to_numeric(df['owners_mid'], errors='coerce')
    df['User score'] = pd.to_numeric(df['User score'], errors='coerce')
    df['Peak CCU'] = pd.to_numeric(df['Peak CCU'], errors='coerce')
    df['is_free'] = df['Price'] == 0
    df['Genres'] = df['Genres'].fillna('').apply(parse_list_string)
    df['main_genre'] = df['Genres'].apply(lambda x: x[0] if x else 'Unknown')
    df['Genre'] = df['main_genre']
    df['successful'] = pd.to_numeric(df['successful'], errors='coerce').fillna(0).astype(int)
    if df['successful'].sum() == 0:
        df['successful'] = ((df['high_owners'].astype(int) + df['high_score'].astype(int) + df['high_ccu'].astype(int)) >= 2).astype(int)
    return df


@st.cache_data
def load_cleaned_data():
    df = pd.read_csv(CLEANED_PATH)
    df['Release date'] = pd.to_datetime(df['Release date'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['owners_mid'] = pd.to_numeric(df['owners_mid'], errors='coerce')
    df['User score'] = pd.to_numeric(df['User score'], errors='coerce')
    df['Peak CCU'] = pd.to_numeric(df['Peak CCU'], errors='coerce')
    df['Genres'] = df['Genres'].fillna('').apply(parse_list_string)
    df['main_genre'] = df['Genres'].apply(lambda x: x[0] if x else 'Unknown')
    df['is_free'] = df['Price'] == 0
    df['successful'] = pd.to_numeric(df['successful'], errors='coerce').fillna(0).astype(int)
    return df


def overview_page():
    df = load_data()

    st.title("Steam Game Success Dashboard")
    st.write(
        "Explore which Steam games are successful based on owners, user score, and peak concurrent users. "
        "Use the filters to compare genre, price, and release period."
    )

    with st.sidebar:
        st.header("Filters")
        min_year = int(df['Release date'].dt.year.min())
        max_year = int(df['Release date'].dt.year.max())
        year_range = st.slider("Release Year", min_year, max_year, (min_year, max_year))

        price_selection = st.slider("Price range", float(df['Price'].min()), float(df['Price'].max()), (0.0, float(df['Price'].quantile(0.95))))
        free_paid = st.selectbox("Game type", ["All", "Free", "Paid"])

        genre_options = sorted({genre for genres in df['Genres'] for genre in genres if genre})
        selected_genres = st.multiselect("Genres", genre_options, default=genre_options[:8])

        success_option = st.selectbox("Success filter", ["All", "Successful games only", "Not successful"])

    filtered = df.copy()
    filtered = filtered[(filtered['Release date'].dt.year >= year_range[0]) & (filtered['Release date'].dt.year <= year_range[1])]
    filtered = filtered[(filtered['Price'] >= price_selection[0]) & (filtered['Price'] <= price_selection[1])]

    if free_paid == "Free":
        filtered = filtered[filtered['is_free']]
    elif free_paid == "Paid":
        filtered = filtered[~filtered['is_free']]

    if selected_genres:
        filtered = filtered[filtered['Genres'].apply(lambda genres: bool(set(genres) & set(selected_genres)))]

    if success_option == "Successful games only":
        filtered = filtered[filtered['successful'] == 1]
    elif success_option == "Not successful":
        filtered = filtered[filtered['successful'] == 0]

    if filtered.empty:
        st.warning("No games match the selected filters. Try adjusting the release year, genre, or success filter.")
        return

    def format_metric(value, fmt="{:,.0f}", na_text="N/A"):
        return na_text if pd.isna(value) else fmt.format(value)

    st.subheader("Key metrics")
    total_games = len(filtered)
    avg_owners = filtered['owners_mid'].mean()
    avg_score = filtered['User score'].mean()
    avg_ccu = filtered['Peak CCU'].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Filtered games", total_games)
    col2.metric("Average owners", format_metric(avg_owners))
    col3.metric("Average user score", format_metric(avg_score, "{:.1f}"))
    col4.metric("Average peak CCU", format_metric(avg_ccu))

    st.markdown("---")

    st.subheader("Genre performance")
    genre_summary = (
        filtered.groupby('main_genre')
        .agg(average_owners=('owners_mid', 'mean'), average_score=('User score', 'mean'), count=('Name', 'nunique'))
        .rename_axis('Genre')
        .sort_values('average_owners', ascending=False)
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=genre_summary.head(12), x='average_owners', y='Genre', palette='viridis', ax=ax)
    ax.set_xlabel('Average Owners')
    ax.set_ylabel('Genre')
    ax.set_title('Top Genres by Average Owners')
    st.pyplot(fig)

    st.subheader("Price vs Owners")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered.sample(min(1500, len(filtered))), x='Price', y='owners_mid', hue='is_free', alpha=0.6, ax=ax)
    ax.set_xlabel('Price')
    ax.set_ylabel('Owners Midpoint')
    ax.set_title('Price vs Owners by Free/Paid')
    ax.legend(title='Free?')
    st.pyplot(fig)

    st.markdown("---")

    st.subheader("Free vs Paid success")
    free_paid_summary = (
        filtered.groupby('is_free')
        .agg(average_owners=('owners_mid', 'mean'), average_score=('User score', 'mean'))
        .rename(index={True: 'Free', False: 'Paid'})
    )
    st.bar_chart(free_paid_summary[['average_owners', 'average_score']])

    st.markdown("---")

    st.subheader("Release year trend")
    time_summary = (
        filtered.groupby(filtered['Release date'].dt.year)
        .agg(average_owners=('owners_mid', 'mean'), average_score=('User score', 'mean'))
        .rename_axis('Year')
        .reset_index()
    )
    st.line_chart(time_summary.set_index('Year')[['average_owners', 'average_score']])

    st.markdown("---")
    st.subheader("Top games by owners")
    st.dataframe(filtered[['Name', 'Genre', 'Price', 'owners_mid', 'User score', 'Peak CCU']].sort_values('owners_mid', ascending=False).head(20))

    st.markdown("---")
    st.write("Data source: Steam games dataset, cleaned and prepared in notebooks.")


def modeling_page():

    df_clean = load_cleaned_data()

    st.title("Modeling & Clustering Insights")
    st.write(
        "This page shows simplified model performance and clustering insights for Steam game success metrics. "
        "The results are based on features like price, user score, and peak concurrent users."
    )

    sample = df_clean.sample(n=min(10000, len(df_clean)), random_state=42)
    sample = sample.dropna(subset=['Price', 'User score', 'Peak CCU', 'high_owners'])

    st.markdown("### Classification model")
    st.write("Predicting whether a game is in the high-owners group using a random forest classifier.")

    features = ['Price', 'User score', 'Peak CCU']
    X = sample[features]
    y = sample['high_owners'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose().round(3)
    report_df.index = report_df.index.astype(str)
    report_display = report_df.loc[report_df.index.isin(['0', '1', 'accuracy']), ['precision', 'recall', 'f1-score']]

    col1, col2 = st.columns(2)
    col1.metric("Accuracy", f"{accuracy:.3f}")
    col2.write("#### Classification report")
    col2.dataframe(report_display)

    importances = pd.Series(clf.feature_importances_, index=features).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=importances.values, y=importances.index, palette='mako', ax=ax)
    ax.set_title('Feature Importances')
    ax.set_xlabel('Importance')
    ax.set_ylabel('Feature')
    st.pyplot(fig)

    st.markdown("---")
    st.markdown("### Clustering")
    st.write("K-means clusters are fit on price, owners midpoint, user score, and peak CCU.")

    cluster_features = ['Price', 'owners_mid', 'User score', 'Peak CCU']
    cluster_df = sample[cluster_features].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(cluster_df)
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    sample['cluster'] = clusters

    cluster_summary = (
        sample.groupby('cluster')
        .agg(count=('Name', 'nunique'),
             avg_owners=('owners_mid', 'mean'),
             avg_score=('User score', 'mean'),
             avg_price=('Price', 'mean'))
        .round(1)
        .reset_index()
    )

    st.dataframe(cluster_summary)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=sample, x='Price', y='owners_mid', hue='cluster', palette='tab10', alpha=0.6, ax=ax)
    ax.set_xlabel('Price')
    ax.set_ylabel('Owners Midpoint')
    ax.set_title('Clusters: Price vs Owners')
    st.pyplot(fig)

    st.markdown("---")
    st.write("Cluster characteristics help show how game success patterns separate by price, owners, and score.")


def main():
    page = st.sidebar.radio("Page", ["Overview", "Model & Clustering"])

    if page == "Overview":
        overview_page()
    else:
        modeling_page()


if __name__ == '__main__':
    main()
