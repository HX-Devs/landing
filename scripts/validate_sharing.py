#!/usr/bin/env python3
"""Validate static sharing metadata and its local assets. No dependencies or network."""
import json
import struct
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.meta = {}
        self.links = []
        self.json_scripts = []
        self.capture_json = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'head':
            self.in_head = True
        if not self.in_head:
            return
        if tag == 'meta':
            key = attrs.get('property', attrs.get('name'))
            self.meta.setdefault(key, []).append(attrs.get('content', ''))
        if tag == 'link':
            self.links.append(attrs)
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.capture_json = True
            self.json_scripts.append('')

    def handle_data(self, data):
        if self.capture_json:
            self.json_scripts[-1] += data

    def handle_endtag(self, tag):
        if tag == 'script':
            self.capture_json = False
        if tag == 'head':
            self.in_head = False


def require(condition, message):
    if not condition:
        raise ValueError(message)


def png_size(path):
    data = path.read_bytes()
    require(data[:8] == b'\x89PNG\r\n\x1a\n', f'Not a PNG: {path}')
    return struct.unpack('>II', data[16:24])


def validate():
    base = 'https://' + (ROOT / 'CNAME').read_text().strip() + '/'
    head = Head()
    head.feed((ROOT / 'index.html').read_text())
    required = (
        'description', 'og:title', 'og:type', 'og:site_name', 'og:locale',
        'og:description', 'og:url', 'og:image', 'og:image:secure_url',
        'og:image:type', 'og:image:width', 'og:image:height', 'og:image:alt',
        'twitter:card', 'twitter:title', 'twitter:description',
        'twitter:image', 'twitter:image:alt',
    )
    for key in required:
        values = head.meta.get(key, [])
        require(len(values) == 1 and values[0].strip(), f'Missing or duplicate head metadata: {key}')
    value = lambda key: head.meta[key][0]
    canonicals = [link.get('href') for link in head.links if link.get('rel') == 'canonical']
    require(canonicals == [base], 'Canonical URL must match CNAME')
    require(value('og:url') == base, 'og:url must match CNAME')
    require(value('og:type') == 'website', 'Expected website Open Graph type')
    image_url = base + 'assets/social-preview.png?v=hx-only'
    for key in ('og:image', 'og:image:secure_url', 'twitter:image'):
        require(value(key) == image_url, f'{key} must use the absolute preview URL')
    require(value('og:image:type') == 'image/png', 'Preview MIME type must be image/png')
    declared = (int(value('og:image:width')), int(value('og:image:height')))
    require(declared == png_size(ROOT / 'assets/social-preview.png') == (1200, 630), 'Wrong preview dimensions')
    require((ROOT / 'assets/social-preview.png').stat().st_size < 5_000_000, 'Preview image is too large')
    require(value('twitter:card') == 'summary_large_image', 'Expected a large-image X card')
    for link in head.links:
        href = link.get('href', '')
        if href and not urlparse(href).scheme and not href.startswith('#'):
            require((ROOT / href).is_file(), f'Broken head asset link: {href}')
    require(any(link.get('rel') == 'apple-touch-icon' for link in head.links), 'Missing Apple Touch icon')
    for size in (32, 180, 192, 512):
        require(png_size(ROOT / f'assets/icon-{size}.png') == (size, size), f'Wrong {size}px icon dimensions')
    manifest = json.loads((ROOT / 'site.webmanifest').read_text())
    for icon in manifest['icons']:
        actual = png_size(ROOT / icon['src'])
        require(icon['sizes'] == f'{actual[0]}x{actual[1]}', f'Manifest icon size mismatch: {icon["src"]}')
    require(bool(head.json_scripts), 'Missing structured data')
    for source in head.json_scripts:
        data = json.loads(source)
        for entity in data.get('@graph', []):
            require(entity.get('url') == base, 'Structured data URL must match CNAME')
            if entity.get('@type') == 'Organization':
                require(entity['logo']['url'] == base + 'assets/icon-512.png', 'Wrong structured logo URL')
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    locations = [e.text for e in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    require(locations == [base], 'Sitemap URL must match CNAME')
    print('PASS: static Open Graph/X cards, canonical URL, preview PNG, icons, manifest, JSON-LD and sitemap.')


if __name__ == '__main__':
    try:
        validate()
    except (ValueError, KeyError, OSError, ET.ParseError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
