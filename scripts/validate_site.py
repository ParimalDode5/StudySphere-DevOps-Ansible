
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import re
import sys


class StudySphereParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = set()
        self.stylesheets = []
        self.scripts = []
        self.title = ""
        self.in_title = False
        self.course_cards = 0
        self.course_buttons = 0

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        attrs = dict(attrs)

        if tag == "title":
            self.in_title = True

        if tag == "link":
            rel = attrs.get("rel", "").lower().split()
            href = attrs.get("href")

            if "stylesheet" in rel and href:
                self.stylesheets.append(href)

        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])

        classes = attrs.get("class", "").split()

        if "course-card" in classes:
            self.course_cards += 1

        if tag == "button" and "data-course" in attrs:
            self.course_buttons += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def validate_site(site_dir):
    site_dir = Path(site_dir)
    errors = []

    print("========== STUDYSPHERE TESTS ==========")

    required_files = [
        "index.html",
        "style.css",
        "script.js"
    ]

    for filename in required_files:
        file_path = site_dir / filename

        if file_path.is_file() and file_path.stat().st_size > 0:
            print(f"PASS: {filename} exists")
        else:
            errors.append(f"Missing or empty file: {filename}")

    if errors:
        raise SystemExit("\n".join(errors))

    html = (site_dir / "index.html").read_text(encoding="utf-8")
    css = (site_dir / "style.css").read_text(encoding="utf-8")
    js = (site_dir / "script.js").read_text(encoding="utf-8")

    parser = StudySphereParser()
    parser.feed(html)
    parser.close()

    for tag in ["html", "head", "body", "main"]:
        if tag in parser.tags:
            print(f"PASS: HTML contains <{tag}>")
        else:
            errors.append(f"Missing HTML element: {tag}")

    if parser.title.strip():
        print("PASS: Page title is present")
    else:
        errors.append("Page title is missing")

    for reference in parser.stylesheets + parser.scripts:
        parsed = urlsplit(reference)

        if parsed.scheme or reference.startswith("//"):
            continue

        if not parsed.path:
            continue

        resource = (site_dir / parsed.path.lstrip("/")).resolve()

        if resource.is_file() and site_dir.resolve() in resource.parents:
            print(f"PASS: Resource found: {parsed.path}")
        else:
            errors.append(f"Missing local resource: {reference}")

    if parser.course_cards >= 6:
        print(f"PASS: {parser.course_cards} course cards found")
    else:
        errors.append("Expected at least 6 course cards")

    if parser.course_buttons >= 6:
        print(f"PASS: {parser.course_buttons} course buttons found")
    else:
        errors.append("Expected at least 6 course buttons")

    clean_css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)

    if clean_css.count("{") == clean_css.count("}"):
        print("PASS: CSS braces are balanced")
    else:
        errors.append("CSS braces are unbalanced")

    if js.strip():
        print("PASS: JavaScript file is not empty")
    else:
        errors.append("JavaScript file is empty")

    if errors:
        print("\n========== TEST FAILED ==========")

        for error in errors:
            print(f"FAIL: {error}")

        raise SystemExit(1)

    print("\n========== ALL TESTS PASSED ==========")


if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else "website"
    validate_site(directory)
