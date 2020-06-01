import logging
import re
import collections
from typing import List, Optional, Mapping, TypeVar, Any

from wostools.fields import parse_all

logger = logging.getLogger(__name__)

# The null part accounts for an ISI wok bug
ISI_LINE_PATTERN = re.compile(r"^(null)?((?P<field>[A-Z0-9]{2})|  )( (?P<value>.*))?$")

ISI_CITATION_PATTERN = re.compile(
    r"""^(?P<AU>[^,]+)?,[ ]         # First author
        (?P<PY>\d{4})?,[ ]          # Publication year
        (?P<J9>[^,]+)?              # Journal
        (,[ ]V(?P<VL>[\w\d-]+))?    # Volume
        (,[ ][Pp](?P<BP>\d+))?      # Start page
        (,[ ]DOI[ ](?P<DI>.+))?     # The all important DOI
        """,
    re.X,
)


class Article(object):
    def __init__(
        self,
        title: Optional[str],
        authors: List[str],
        year: Optional[int],
        journal: Optional[str],
        volume: Optional[str] = None,
        page: Optional[str] = None,
        doi: Optional[str] = None,
        references: Optional[List[str]] = None,
        sources: Optional[List[str]] = None,
        extra: Optional[Mapping] = None,
    ):
        self.title: Optional[str] = title
        self.authors: List[str] = authors
        self.year: Optional[int] = year
        self.journal: Optional[str] = journal
        self.volume: Optional[str] = volume
        self.page: Optional[str] = page
        self.doi: Optional[str] = doi
        self.references: List[str] = references or []
        self.sources: List[str] = sources or []
        self.extra: Mapping[str, Any] = extra or {}

    @property
    def label(self):
        if not (self.authors and self.year and self.journal):
            raise ValueError("Missing required fields for label")
        pieces = {
            "AU": self.authors[0].replace(",", ""),
            "PY": str(self.year),
            "J9": str(self.journal),
            "VL": f"V{self.volume}" if self.volume else None,
            "BP": f"P{self.page}" if self.page else None,
            "DI": f"DOI {self.doi}" if self.doi else None,
        }
        return ", ".join(value for value in pieces.values() if value)

    def merge(self, other: "Article") -> "Article":
        if self.label != other.label:
            logger.warning(
                "Mixing articles with different labels might result in tragedy"
            )
        return Article(
            title=self.title or other.title,
            authors=list(set(self.authors).union(set(other.authors))),
            year=self.year or other.year,
            journal=self.journal or other.journal,
            volume=self.volume or other.volume,
            page=self.page or other.page,
            doi=self.doi or other.doi,
            sources=[*self.sources, *other.sources],
            extra={**self.extra, **other.extra},
        )

    @classmethod
    def from_isi_text(cls, raw: str) -> "Article":
        data = collections.defaultdict(list)
        field = None
        for line in raw.split("\n"):
            match = ISI_LINE_PATTERN.match(line)
            if not match:
                raise ValueError(f"'{line}' is not a valid ISI file line")
            parsed = match.groupdict()
            field = parsed.get("field") or field
            if not field or "value" not in parsed or parsed["value"] is None:
                continue
            data[field].append(parsed["value"])
        processed = parse_all(dict(data))
        return cls(
            title=processed.get("title"),
            authors=processed.get("authors", []),
            year=processed.get("year"),
            journal=processed.get("source_abbreviation"),
            volume=processed.get("volume"),
            page=processed.get("beginning_page"),
            doi=processed.get("DOI"),
            references=processed.get("references"),
            extra=processed,
            sources=[raw],
        )

    @classmethod
    def from_isi_citation(cls, citation: str) -> "Article":
        match = ISI_CITATION_PATTERN.match(citation)
        if not match:
            raise ValueError(f"{citation} does not look like an ISI citation")
        data = {key: [value] for key, value in match.groupdict().items() if value}
        processed = parse_all(data)
        return cls(
            title=processed.get("title"),
            authors=processed.get("authors", []),
            year=processed.get("year"),
            journal=processed.get("source_abbreviation"),
            volume=processed.get("volume"),
            page=processed.get("beginning_page"),
            doi=processed.get("DOI"),
            extra=processed,
            sources=[citation],
        )
