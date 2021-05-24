import collections
import re
from typing import Iterable, TextIO
from wostools.exceptions import InvalidIsiLine, InvalidReference
from wostools.article import Article
from wostools.fields import parse_all

ISI_LINE_PATTERN = re.compile(
    r"^(null|.)?((?P<field>[A-Z0-9]{2})|  )( (?P<value>.*))?$"
)

ISI_CITATION_PATTERN = re.compile(
    r"""^(?P<AU>[^,]+),[ ]          # First author
        (?P<PY>\d{4}),[ ]           # Publication year
        (?P<J9>[^,]+)               # Journal
        (,[ ]V(?P<VL>[\w\d-]+))?    # Volume
        (,[ ][Pp](?P<BP>\w+))?      # Start page
        (,[ ]DOI[ ](?P<DI>.+))?     # The all important DOI
        """,
    re.X,
)


def _split(file) -> Iterable[str]:
    parts = file.read().split("\n\n")
    for part in parts:
        if part != "ER":
            yield part


def parse_file(file: TextIO) -> Iterable[Article]:
    for raw in _split(file):
        yield Article.from_isi_text(raw)


def parse_record(record: str) -> Article:
    """
    Transforms an isi record in text form into a fully concrete article.
    """
    data = collections.defaultdict(list)
    field = None
    for line in record.split("\n"):
        match = ISI_LINE_PATTERN.match(line)
        if not match:
            raise InvalidIsiLine(line)
        parsed = match.groupdict()
        field = parsed.get("field") or field
        if not field or "value" not in parsed or parsed["value"] is None:
            continue
        data[field].append(parsed["value"])
    processed = parse_all(dict(data))

    authors = [a.replace(",", "") for a in processed.get("authors", [])]
    references = [parse_label(r) for r in processed.get("references", [])]

    # TODO: think what we lose without sub-classing.
    return Article(
        title=processed.get("title"),
        authors=authors,
        year=processed.get("year"),
        journal=processed.get("source_abbreviation"),
        volume=processed.get("volume"),
        issue=processed.get("issue"),
        page=processed.get("beginning_page"),
        doi=processed.get("DOI"),
        references=references,
        keywords=processed.get("keywords"),
        extra=processed,
        sources={record},
    )


def parse_label(label: str) -> Article:
    match = ISI_CITATION_PATTERN.match(label)
    if not match:
        raise InvalidReference(label)
    data = {key: [value] for key, value in match.groupdict().items() if value}
    processed = parse_all(data)
    return Article(
        title=processed.get("title"),
        authors=processed.get("authors", []),
        year=processed.get("year"),
        journal=processed.get("source_abbreviation"),
        volume=processed.get("volume"),
        page=processed.get("beginning_page"),
        doi=processed.get("DOI"),
        extra=processed,
        sources={label},
    )
