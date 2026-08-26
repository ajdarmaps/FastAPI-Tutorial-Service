from uuid import UUID


def build_posts_list_cache_key(
    page: int,
    page_size: int,
    search: str | None,
    author_id: UUID | None,
) -> str:
    normalized_search = search.strip().lower() if search else "none"

    normalized_author = str(author_id) if author_id is not None else "none"

    return (
        f"posts:list:"
        f"page={page}:"
        f"size={page_size}:"
        f"search={normalized_search}:"
        f"author={normalized_author}"
    )
