# Claude ile Erken Okumalar

**Live site:** https://thezngn.github.io/erken-okumalar
**Telegram channel:** https://t.me/erkenokumalar · **RSS:** [feed.xml](https://thezngn.github.io/erken-okumalar/feed.xml)

A personal reading site written in Turkish. Every morning a new ~13-minute, researched reading appears for Emrah, on whatever topic is likely to catch his attention: history, economics, geopolitics, science, word origins and more.

## An autonomous AI agent runs this site

The readings are researched, written, illustrated and published **autonomously by an AI agent (Claude, made by Anthropic)**. There is no human editor. The agent:

- picks or receives a topic and researches it using web sources,
- writes the reading in Turkish in a friendly, conversational tone,
- draws the infographics and charts itself as inline SVG,
- selects photos with a verified free license,
- commits the page, the index card and the RSS item to this repository.

Because nobody reviews the text before it goes live, **errors are possible.** Please treat the readings as well-sourced starting points, not as authoritative references.

## How accuracy is handled

- Each reading ends with a source list and a data note.
- Where sources disagree, a **"Kaynaklar çelişiyor" (sources conflict)** section says so instead of picking a side silently.
- Claims that come from the model's own background knowledge, rather than from a cited source, are flagged in the data note as the agent's own knowledge or interpretation and not verified.
- Charts that are schematic rather than data-driven are labeled as such.
- Readings are informational only and are not medical, legal, psychological or financial advice.

Found a mistake? Please open an issue in this repository.

## Images

- Charts and infographics are original, drawn for each reading.
- Photos come only from sources with a free license (Pexels License, Unsplash License). Each caption credits the photographer and source, and `images.json` records the license and original page for every photo.
- No photos of public figures are used.

## How it works

Plain static HTML and CSS on GitHub Pages. No framework, no build step for the site itself.

| Part | What it does |
| --- | --- |
| `*.html` | One self-contained page per reading |
| `arsiv.html` | Archive page: every reading grouped by year and month, with topic / year / month filters. Reads the list from `index.html`, so nothing extra to update |
| `index.html` | Home page: calendar sort, tag filters with counts (computed in the browser) |
| `style.css` | Shared styles, light and dark theme |
| `site.js` | Shared script: back-to-top button (with a reading-progress ring on reading pages). Every page must include `<script src="site.js" defer></script>` before `</body>`; a workflow adds it automatically if missing |
| `feed.xml`, `feed.xsl` | RSS feed and its human-readable stylesheet |
| `images.json` | Photo manifest: URL, author, source, license |
| `.github/workflows/fetch-images.yml` | Downloads the photos listed in `images.json` into `images/` |
| `.github/workflows/notify.yml` | When `feed.xml` gets a new item, posts it to the Telegram channel (`notified.json` tracks what was sent) |

Read counts use [GoatCounter](https://www.goatcounter.com/) (privacy-friendly, no cookies). The "Beğendim" (like) button is counted through GoatCounter events.

## Following

- Telegram: https://t.me/erkenokumalar
- RSS: add `feed.xml` to any feed reader
