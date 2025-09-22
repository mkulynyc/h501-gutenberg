import pandas as pd

def load_data():
    """
    This function loads the authors, metadata, and languages data from a GitHub repository.
    
    Arguments:
        None

    Returns:
        pandas DataFrames containing authors, metadata, and languages data
    """
    authors = pd.read_csv(
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_authors.csv"
    )
    metadata = pd.read_csv(
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_metadata.csv"
    )
    languages = pd.read_csv(
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_languages.csv"
    )
    return authors, metadata, languages


def count_translations_by_author(authors, metadata, languages, alias=True):
    """
    Count number of translations per author.

    Arguments:
        authors: dataframe
        metadata: dataframe
        languages: dataframe
        alias: bool -> use author alias column if True, else use author name

    Returns:
        DataFrame with author + translation count
    """
    # merge metadata with languages
    meta_lang = metadata.merge(languages, on="gutenberg_id", how="left")

    # count number of unique languages per book
    lang_counts = (
        meta_lang.groupby("gutenberg_id")["language_y"]
        .nunique()
        .reset_index(name="num_languages")
    )

    # attach to authors
    merged = metadata.merge(authors, on="author_id", how="left").merge(
        lang_counts, on="gutenberg_id", how="left"
    )

    # translations = languages - 1 (ignore original)
    merged["translations"] = merged["num_languages"].fillna(1) - 1

    group_col = "alias" if alias else "name"
    out = (
        merged.groupby(group_col)["translations"]
        .sum()
        .reset_index()
        .sort_values("translations", ascending=False)
    )

    return out
