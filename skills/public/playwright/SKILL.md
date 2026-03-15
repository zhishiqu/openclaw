---
name: playwright
description: Web page fetching and scraping using Playwright browser automation. Use when: (1) fetching content from JavaScript-rendered pages, (2) bypassing basic anti-bot measures, (3) extracting text from complex websites, (4) WeChat articles and other protected content, (5) any URL content extraction that fails with simple HTTP requests.
---

# Playwright Web Fetching

Fetch and extract content from web pages using browser automation.

## When to Use

Use this skill when:

- Simple `curl` or HTTP requests fail (captcha, JavaScript rendering, anti-bot)
- Need to fetch WeChat articles, dynamic websites
- Page requires JavaScript to render content
- Need to simulate real browser behavior

## Quick Start

### Fetch a URL

```bash
python3 scripts/fetch_url.py <url> [wait_time_ms]
```

**Examples:**

```bash
# Fetch WeChat article
python3 scripts/fetch_url.py "https://mp.weixin.qq.com/s/xxx" 3000

# Fetch with longer wait for dynamic content
python3 scripts/fetch_url.py "https://example.com" 5000
```

### Output Format

```json
{
  "success": true,
  "url": "https://...",
  "title": "Page Title",
  "content": "Extracted text content...",
  "error": ""
}
```

## Scripts

| Script                 | Purpose                                |
| ---------------------- | -------------------------------------- |
| `scripts/fetch_url.py` | Fetch single URL, extract text content |

## Usage Patterns

### Pattern 1: WeChat Articles

```bash
python3 scripts/fetch_url.py "https://mp.weixin.qq.com/s/xxx" 3000
```

### Pattern 2: JavaScript-Heavy Sites

```bash
python3 scripts/fetch_url.py "https://dynamic-site.com" 5000
```

### Pattern 3: Extract and Summarize

After fetching, use the content to:

- Summarize the article
- Extract key points
- Organize into structured format

## Dependencies

Install Playwright:

```bash
pip install playwright
playwright install chromium
```

## Troubleshooting

**Issue: Page still shows captcha**

- Increase wait_time to 5000ms
- Some sites have stronger anti-bot that requires more advanced techniques

**Issue: Content is empty**

- Try different wait_time values
- Page may require user interaction (not supported yet)

**Issue: Timeout errors**

- Increase timeout in script (default 60s)
- Check network connectivity
