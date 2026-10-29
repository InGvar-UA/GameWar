"""Build two crawlable static language pages from the Ukrainian source."""
from pathlib import Path
from lxml import html, etree
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parent
NODE = os.environ.get("NODE_BIN", "node")
SITE_URL = os.environ.get("SITE_URL", "https://gamewar.fun/").rstrip("/") + "/"
script = (ROOT / "script.js").read_text(encoding="utf-8")
match = re.search(r"const translations = (\{[\s\S]*?\n\});\n\ndocument\.querySelectorAll", script)
if not match:
    raise RuntimeError("Could not find translations in script.js")
js = "const vm=require('vm');const d=vm.runInNewContext('('+process.argv[1]+')');console.log(JSON.stringify(d))"
translations = json.loads(subprocess.check_output([NODE, "-e", js, match.group(1)], text=True, encoding="utf-8"))


def set_inner(element, markup):
    element.clear()
    for child in html.fragments_fromstring(markup):
        if isinstance(child, str):
            if len(element):
                element[-1].tail = (element[-1].tail or "") + child
            else:
                element.text = (element.text or "") + child
        else:
            element.append(child)


def add_meta(head, name, content, prop=False):
    item = etree.Element("meta")
    item.set("property" if prop else "name", name)
    item.set("content", content)
    head.append(item)


def add_link(head, rel, href, hreflang=None):
    item = etree.Element("link")
    item.set("rel", rel)
    item.set("href", href)
    if hreflang:
        item.set("hreflang", hreflang)
    head.append(item)


source = html.fromstring((ROOT / "index.html").read_text(encoding="utf-8"))
for lang in ("uk", "ru"):
    doc = html.fromstring(etree.tostring(source, encoding="unicode"))
    doc.set("lang", lang)
    head = doc.find("head")
    for stale in head.xpath('./link[@rel="canonical" or @rel="alternate"] | ./meta[starts-with(@property,"og:") or @name="twitter:card"]'):
        head.remove(stale)
    title = "З ким пограти в Call of Duty на PS5 — команда для Warzone і DMZ | GameWar" if lang == "uk" else "С кем поиграть в Call of Duty на PS5 — команда для Warzone и DMZ | GameWar"
    description = (
        "Шукаєш тімейтів для Call of Duty на PS5? Знайди загін для Modern Warfare 4, DMZ та Warzone в Discord-спільноті GameWar."
        if lang == "uk" else
        "Ищешь тиммейтов для Call of Duty на PS5? Найди отряд для Modern Warfare 4, DMZ и Warzone в Discord-сообществе GameWar."
    )
    head.find("title").text = title
    head.xpath('./meta[@name="description"]')[0].set("content", description)
    for element in doc.xpath("//*[@data-i18n]"):
        key = element.get("data-i18n")
        element.text = translations[lang][key]
    for element in doc.xpath("//*[@data-i18n-html]"):
        key = element.get("data-i18n-html")
        old = dict(element.attrib)
        set_inner(element, translations[lang][key])
        element.attrib.update(old)
    for element in doc.xpath('//*[@data-lang]'):
        current = element.get("data-lang") == lang
        element.set("aria-pressed", "true" if current else "false")
        classes = element.get("class", "").replace("active", "").strip()
        element.set("class", (classes + " active").strip() if current else classes)
    for element in doc.xpath('//*[@data-lang="uk"]'):
        element.set("data-target", "/" if lang == "ru" else "")
    for element in doc.xpath('//*[@data-lang="ru"]'):
        element.set("data-target", "/ru/" if lang == "uk" else "")

    if lang == "ru":
        head.xpath('./link[@rel="stylesheet"]')[0].set("href", "../styles.css")
        doc.xpath('//script[@src="script.js"]')[0].set("src", "../script.js")
        for image in doc.xpath('//img[@src]'):
            image.set("src", "../" + image.get("src"))
    # The same external destination is used for both localized pages.
    for link in doc.xpath('//a[contains(concat(" ", normalize-space(@class), " "), " discord-link ")]'):
        link.set("href", "https://discord.com/invite/mzwFcDHk5Z")
        link.set("target", "_blank")
        link.set("rel", "noopener noreferrer")
    canonical = SITE_URL if lang == "uk" else SITE_URL + "ru/"
    add_link(head, "canonical", canonical)
    add_link(head, "alternate", SITE_URL, "uk")
    add_link(head, "alternate", SITE_URL + "ru/", "ru")
    add_link(head, "alternate", SITE_URL, "x-default")
    add_meta(head, "og:type", "website", True)
    add_meta(head, "og:site_name", "GameWar", True)
    add_meta(head, "og:locale", "uk_UA" if lang == "uk" else "ru_RU", True)
    add_meta(head, "og:title", title, True)
    add_meta(head, "og:description", description, True)
    add_meta(head, "og:url", canonical, True)
    add_meta(head, "og:image", SITE_URL + "assets/operators-official.webp", True)
    add_meta(head, "twitter:card", "summary_large_image")

    output = ROOT / ("index.html" if lang == "uk" else "ru/index.html")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(etree.tostring(doc, encoding="utf-8", method="html", doctype="<!doctype html>"))

(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + SITE_URL + "sitemap.xml\n", encoding="utf-8")
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '  <url><loc>' + SITE_URL + '</loc></url>\n'
    '  <url><loc>' + SITE_URL + 'ru/</loc></url>\n'
    '</urlset>\n', encoding="utf-8")
