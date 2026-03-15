#!/usr/bin/env python3
"""
Fetch webpage content using Playwright.
Handles JavaScript-rendered pages, bypasses some anti-bot measures.
"""

import asyncio
import sys
import json
from playwright.async_api import async_playwright

async def fetch_url(url: str, wait_time: int = 2000, full_page: bool = True):
    """
    Fetch webpage content using Playwright.
    
    Args:
        url: URL to fetch
        wait_time: Time to wait after page load (ms)
        full_page: Whether to wait for full page load
    
    Returns:
        dict with title, content, url, success status
    """
    result = {
        "success": False,
        "url": url,
        "title": "",
        "content": "",
        "error": ""
    }
    
    try:
        async with async_playwright() as p:
            # Launch browser with stealth options
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                ]
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                bypass_csp=True
            )
            
            page = await context.new_page()
            
            # Add stealth scripts
            await page.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            ''')
            
            # Navigate to page
            await page.goto(url, wait_until='networkidle', timeout=60000)
            
            # Wait for dynamic content
            await page.wait_for_timeout(wait_time)
            
            # Extract title
            result["title"] = await page.title()
            
            # Extract main content
            content = await page.evaluate('''
                () => {
                    // Try to find main content area
                    const selectors = [
                        'article', 
                        '.article-content', 
                        '.post-content',
                        '.content',
                        'main',
                        '[role="main"]'
                    ];
                    
                    let mainContent = null;
                    for (const selector of selectors) {
                        mainContent = document.querySelector(selector);
                        if (mainContent) break;
                    }
                    
                    if (mainContent) {
                        return mainContent.innerText;
                    }
                    
                    // Fallback to body
                    return document.body.innerText;
                }
            ''')
            
            result["content"] = content
            result["success"] = True
            
            await browser.close()
            
    except Exception as e:
        result["error"] = str(e)
    
    return result

async def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: fetch_url.py <url> [wait_time_ms]"
        }))
        return
    
    url = sys.argv[1]
    wait_time = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    
    result = await fetch_url(url, wait_time)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
