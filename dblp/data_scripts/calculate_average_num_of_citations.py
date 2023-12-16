import pandas as pd
from datetime import datetime

# get data dblp author
df_authors_0 = pd.read_csv("../data/analysis/author_dblp/authors_0.csv")
df_authors_1 = pd.read_csv("../data/analysis/author_dblp/authors_1.csv")


df_authors_0_inproc = pd.read_csv("../data/analysis/author_dblp/authors_0_inproc.csv")
df_authors_1_inproc = pd.read_csv("../data/analysis/author_dblp/authors_1_inproc.csv")

df_journals_dblp = pd.concat(
    [
        df_authors_0[df_authors_0["publication_year"] < 2024],
        df_authors_1[df_authors_1["publication_year"] < 2024],
    ]
)
df_conferences_dblp = pd.concat(
    [
        df_authors_0_inproc[df_authors_0_inproc["publication_year"] < 2024],
        df_authors_1_inproc[df_authors_1_inproc["publication_year"] < 2024],
    ]
)

df_all_dblp = pd.concat([df_journals_dblp, df_conferences_dblp])

print(df_all_dblp)


def count_average_citation_for_paper(row):
    current_date = datetime.now().date()

    # print(row)
    publication_date = datetime.strptime(row["publication_date"], "%Y-%m-%d")

    difference_in_years = abs(current_date.year - publication_date.year)

    if difference_in_years <= 1:
        return row["cited_by_count"]
    else:
        return row["cited_by_count"] / difference_in_years


df_all_dblp["average_citation_count"] = df_all_dblp.apply(
    count_average_citation_for_paper, axis=1
)

df_average_citations = (
    df_all_dblp.groupby(["dblp_author_name"])["average_citation_count"]
    .agg(["mean"])
    .reset_index()
)

df_average_citations_sorted = df_average_citations.sort_values(
    by="mean", ascending=False
)

research_age_all = pd.read_csv("../data/research_age/dblp_all.csv")
research_age_all = research_age_all.drop(columns=["Unnamed: 0"])

research_age_and_avg_citations = pd.merge(
    df_average_citations_sorted.head(500).copy(),
    research_age_all,
    on="dblp_author_name",
)  # 'inner' keeps only common values in both DataFrames


research_age_and_avg_citations.to_csv(
    "../data/analysis/authors_avg_citations/authors_avg_citations_all.csv"
)
