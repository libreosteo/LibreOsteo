from haystack.backends.whoosh_backend import WhooshEngine, WhooshSearchBackend
from whoosh.analysis import (
    CharsetFilter,
    LowercaseFilter,
    NgramFilter,
    RegexTokenizer,
    StopFilter,
    StemFilter,
)
from whoosh.support.charset import accent_map

folding_analyzer = (
    RegexTokenizer()
    | LowercaseFilter()
    | CharsetFilter(accent_map)
    | StopFilter()
    | StemFilter()
    | NgramFilter(minsize=2, maxsize=15)
)


def fold_accents(text):
    return "".join(accent_map.get(ord(c), c) for c in text.lower())


class FoldingWhooshSearchBackend(WhooshSearchBackend):
    def build_schema(self, fields):
        content_field_name, schema = super(
            FoldingWhooshSearchBackend, self
        ).build_schema(fields)
        for name, field in schema.items():
            if hasattr(field, "analyzer"):
                field.analyzer = folding_analyzer
        return content_field_name, schema

    def search(self, query_string, **kwargs):
        folded = fold_accents(query_string)
        return super().search(folded, **kwargs)


class FoldingWhooshEngine(WhooshEngine):
    backend = FoldingWhooshSearchBackend
