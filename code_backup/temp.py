import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.webkit.launch()
        page = await browser.new_page()
        await page.goto("https://file-downloader-26b9e.web.app/")
        async with page.expect_download() as download_info:
            await page.get_by_role("button", name="Download text file").click()
        download = await download_info.value
        await download.save_as("downloaded_file.txt")
        await page.screenshot(path="example.png")
        await browser.close()

asyncio.run(main())