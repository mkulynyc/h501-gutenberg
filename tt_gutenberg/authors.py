from .utils import load_data, count_translations_by_author

def list_authors(by_languages=True, alias=True):
    """
    This function returns a list of authors/aliases ordered by number of translations.
    
    Args:
        by_languages: a bool that if True (default) counts translations by number of languages, else counts by number of translated books
        alias: a bool that if True (default) uses the author alias column, else uses the author name column

    Returns:
        A list of tuples (author/alias, translation count)
    """ 
    
    # Load the data
    authors, metadata, languages = load_data()
    
    # If counting by languages
    if by_languages:
        counts = count_translations_by_author(authors, metadata, languages, alias=alias)
        
        # Remove empty or missing aliases
        group_col = "alias" if alias else "author"
        counts = counts[counts[group_col].notna() & (counts[group_col] != "")]
        
        # Return a list of tuples: (alias, translation_count)
        return list(zip(counts[group_col], counts["translations"]))
    
    # Not supporting counting by number of translated books right now
    else:
        raise NotImplementedError("Only by_languages=True is supported right now.")
