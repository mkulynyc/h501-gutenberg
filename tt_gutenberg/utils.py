import pandas as pd

def load_data():
    """
    This function loads the authors, metadata, and languages data from a GitHub repository and returns them as pandas DataFrames.
    
    Arguments:
        None

    Returns:
        pandas DataFrames containing authors, metadata, and languages data
    """
    # Read in authors data
    authors = pd.read_csv(
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_authors.csv"
    )
    
    # Read in metadata
    metadata = pd.read_csv(
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_metadata.csv"
    )
    
    # Read in languages data
    languages = pd.read_csv(
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_languages.csv"
    )
    
    # Return as pandas DFs
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
    # Left merge metadata and languages on gutenberg_id
    meta_lang = metadata.merge(languages, on="gutenberg_id", how="left")

    # count number of unique languages per book
    lang_counts = (
        
        # The merge changed the language column name to language_y
        meta_lang.groupby("gutenberg_id")["language_y"]
        
        # Count the number of unique languages per book
        .nunique()
        .reset_index(name="num_languages")
    )

    # First, merge metadata and authors on gutenberg_author_id, then merge with lang_counts on gutenberg_id
    merged = metadata.merge(authors, left_on="gutenberg_author_id", right_on="gutenberg_author_id", how="left") \
                 .merge(lang_counts, on="gutenberg_id", how="left")


    # Translations = languages - 1 (ignore original)
    merged["translations"] = merged["num_languages"].fillna(1) - 1

    # Group by author alias or name and sum translations, then sort descending to get most translated authors first
    group_col = "alias" if alias else "name"
    out = (
        merged.groupby(group_col)["translations"]
        .sum()
        .reset_index()
        .sort_values("translations", ascending=False)
    )

    return out
