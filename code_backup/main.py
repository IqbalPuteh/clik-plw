import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=True)
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    context = await browser.new_context(user_agent=userAgent, bypass_csp=True)
    page = await context.new_page()
    await page.goto("https://cbsnusantara.cbclik.com/Account/Login")
    await page.get_by_role("textbox", name="Username").fill("NEFO4081")
    await page.get_by_role("textbox", name="Password").fill("Ptfti2025")
    await page.wait_for_load_state("networkidle")
    await page.get_by_role("button", name="Login").click()
    await page.get_by_role("link", name="Company").nth(2).click()
    await page.locator("#CompanyModel_PurposeOfEnquiry").select_option("20")
    await page.locator("#CompanyModel_CompanyDataModel_MessageID").fill("00025FTICREVI2025")
    await page.locator("#CompanyModel_CompanyDataModel_TradeName").fill("PT Prima Tata Solusindo")
    await page.get_by_role("textbox", name="FIELD 'ADDRESS' LENGTH IS NOT").fill("Gedung Graha Pena Jawa Pos Lt.5, Jl Raya Kebayoran Lama No.12")
    await page.get_by_role("textbox", name="FIELD 'SUB DISTRICT' IS").fill("GROGOL UTARA")
    await page.get_by_role("textbox", name="FIELD 'DISTRICT' IS MANDATORY").fill("KEBAYORAN LAMA")
    await page.locator("#CompanyModel_AddressDataModel_City").select_option("0394")
    await page.get_by_role("textbox", name="FIELD 'POSTAL CODE' IS").fill("20146")
    await page.locator("#CompanyModel_AddressDataModel_Country").select_option("ID")
    await page.locator("#CompanyModel_IdentificationCodeModel_BusniessNumber").fill("028822948013000")
    await page.get_by_role("textbox", name="AT LEAST ONE BETWEEN 'PHONE").fill("08119931126")
    await page.get_by_text("Next").click()
    await page.wait_for_load_state("networkidle")
    await page.locator("#ContractModel_IndividualRole").select_option("B")
    await page.locator("#operationCombo").select_option("[[N99,F01],F01]")
    await page.locator("#ContractModel_ContractDataModelCredit_ApplicationAmount").fill("100000000")
    await page.get_by_text("Submit").click()
    #async with page.expect_download() as download_info:
        #await page.get_by_text("Submit").click()
    #download = await download_info.value
    #await download.save_as("downloaded_file.txt")
    await page.wait_for_load_state("networkidle")
    page.set_default_timeout(120000)
    await page.screenshot(path="ss-comp-last-page.png")
    async with page.expect_download() as download_info:
        #async with page.expect_popup() as page1_info:
        await page.get_by_role("link", name=" View PDF").click()
        #page1 = await page1_info.value
    download = await download_info.value
    await download.save_as("downloaded_file.pdf")
    #await page1.close()
    await page.wait_for_load_state("networkidle")
    await page.get_by_role("button", name=" 100192 / 000 / NEFO4081").click()
    await page.get_by_role("link", name=" Logout").click()
    await page.wait_for_load_state("networkidle")

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
