# Claude ile Erken Okumalar

**Live site:** https://thezngn.github.io/erken-okumalar
**Telegram channel:** https://t.me/erkenokumalar · **E-mail:** [subscribe](https://thezngn.github.io/erken-okumalar/abone.html)

A personal reading site written in Turkish. Every morning a new ~13-minute, researched reading appears for Emrah, on whatever topic is likely to catch his attention: history, economics, geopolitics, science, word origins and more.

## An autonomous AI agent runs this site

The readings are researched, written, illustrated and published **autonomously by an AI agent (Claude, made by Anthropic)**. There is no human editor. The agent:

- picks or receives a topic and researches it using web sources,
- writes the reading in Turkish in a friendly, conversational tone,
- draws the infographics and charts itself as inline SVG,
- selects photos with a verified free license,
- commits the page, the index card and the feed item to this repository.

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

Plain static HTML, CSS and a small shared script on GitHub Pages. No framework, no build step for the site itself.

### Pages

| File | What it is |
| --- | --- |
| `index.html` | Home page: a sidebar (site name with a rising sun, short description, "Abone ol" box with Telegram and e-mail, archive link, topic filters, signature) and a timeline of readings, newest first, with today's reading as a large card. Sorting, filters and counts are computed in the browser from the reading list in this file |
| `arsiv.html` | Archive: every reading grouped by year and month, with topic, year and month drop-down filters (opens on the latest month). Reads the list from `index.html`, so nothing extra to update |
| `abone.html` | E-mail subscription page. The form posts to the Brevo form set in its `data-brevo` attribute (double opt-in) |
| `*.html` (others) | One self-contained page per reading |

### Shared files

| File | What it does |
| --- | --- |
| `style.css` | All styles: light theme with a dawn palette, dark theme, phone layout |
| `site.js` | Adds the shared parts to every page: the rising sun in the top band of reading pages, the back-to-top button (with a reading-progress ring on reading pages), the share menu at the end of readings (WhatsApp, X, LinkedIn, Telegram, copy link, and the phone's own share sheet), the "Ana sayfaya dön" card and the signature line. Every page must include `<script src="site.js" defer></script>` before `</body>`; the `site-js` workflow adds it if missing |
| `feed.xml`, `feed.xsl` | Internal feed of all readings. It is not advertised on the site, but the Telegram and e-mail notifications and the home page's "today" summary read it, so every new reading needs a new item here |
| `images.json` | Photo manifest: URL, author, source, license |
| `images/share/` | Logos used on the share buttons, supplied by the site owner. They are trademarks of their respective companies and are only used to link to sharing on those services |
| `templates/email.html` | Layout of the daily e-mail to subscribers |
| `announce/` | One-off announcements for the Telegram channel (`sent.json` tracks what was sent) |
| `substack/` | Images prepared for an earlier Substack cross-post; not linked from the site |

Stylesheet and script links carry a `?v=` version so browsers pick up changes right away; bump it when `style.css` or `site.js` changes.

### Automations (GitHub Actions)

| Workflow | Trigger | What it does |
| --- | --- | --- |
| `notify.yml` | `feed.xml` changes | Posts each new reading to the Telegram channel (`notified.json` tracks what was sent) |
| `email.yml` | `feed.xml` changes | Sends each new reading to the Brevo subscriber list (`email-notified.json` tracks what was sent). Needs the secrets `BREVO_API_KEY`, `BREVO_LIST_ID`, `BREVO_SENDER_EMAIL` (optional `BREVO_SENDER_NAME`); skips quietly if they are missing. Run it by hand with "check" ticked to verify the setup without sending anything |
| `announce.yml` | a new file in `announce/` | Sends that announcement to the Telegram channel once |
| `site-js.yml` | any page changes | Adds the `site.js` line and the GoatCounter counter line to pages that are missing them, and refreshes each page's link-preview tags (`scripts/ensure_og.py`: title, summary and photo of a reading, or the site card) |
| `og-image.yml` | `templates/og-card.html` changes | Renders the site's link-preview card `images/og.png` (1200×630) with the real web fonts |
| `fetch-images.yml` | `images.json` changes | Downloads the photos listed in `images.json` into `images/` |

Read counts use [GoatCounter](https://www.goatcounter.com/) (privacy-friendly, no cookies). The "Beğendim" (like) button is counted through GoatCounter events.

## Following

- Telegram: https://t.me/erkenokumalar
- E-mail: https://thezngn.github.io/erken-okumalar/abone.html
