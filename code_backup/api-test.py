from fastapi import FastAPI, HTTPException
import asyncio, uvicorn
from playwright.sync_api import Playwright, sync_playwright
from config import USERNAME, PASSWORD, LOGIN_URL, HEADLESS
import logging
import time
import os

app = FastAPI()

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Playwright Web API"}

def do(playwright: Playwright) -> str:
    browser =  playwright.chromium.launch()
    context =  browser.new_context()
    page =   context.new_page()
    try:
        page.goto("https://cbsnusantara.cbclik.com/Account/Login")
        page.wait_for_load_state("load")
        page.get_by_role("button", name="").click()
        page.get_by_role("link", name="English").click()
        page.screenshot(path="ss-comp-first-page.png")
        page.get_by_role("textbox", name="Username").fill(USERNAME)
        page.get_by_role("textbox", name="Password").fill(PASSWORD)
        page.get_by_role("button", name="Login").click()
        page.wait_for_load_state("load")
        page.get_by_role("link", name="Company").nth(2).click()
        page.wait_for_load_state("load")
        page.locator("#CompanyModel_PurposeOfEnquiry").select_option("20")
        page.locator("#CompanyModel_CompanyDataModel_MessageID").fill("00025FTICREVI2025")
        page.locator("#CompanyModel_CompanyDataModel_TradeName").fill("PT Prima Tata Solusindo")
        page.get_by_role("textbox", name="FIELD 'ADDRESS' LENGTH IS NOT").fill("Gedung Graha Pena Jawa Pos Lt.5, Jl Raya Kebayoran Lama No.12")
        page.get_by_role("textbox", name="FIELD 'SUB DISTRICT' IS").fill("GROGOL UTARA")
        page.get_by_role("textbox", name="FIELD 'DISTRICT' IS MANDATORY").fill("KEBAYORAN LAMA")
        page.locator("#CompanyModel_AddressDataModel_City").select_option("0394")
        page.get_by_role("textbox", name="FIELD 'POSTAL CODE' IS").fill("20146")
        page.locator("#CompanyModel_AddressDataModel_Country").select_option("ID")
        page.locator("#CompanyModel_IdentificationCodeModel_BusniessNumber").fill("028822948013000")
        page.get_by_role("textbox", name="AT LEAST ONE BETWEEN 'PHONE").fill("08119931126")
        page.wait_for_load_state("load")
        page.get_by_text("Next").click()
        page.wait_for_load_state("load")
        page.locator("#ContractModel_IndividualRole").select_option("B")
        page.locator("#operationCombo").select_option("[[N99,F01],F01]")
        page.locator("#ContractModel_ContractDataModelCredit_ApplicationAmount").fill("100000000")
        page.get_by_text("Submit").click()
        page.wait_for_load_state("load")
        page.set_default_timeout(120000)
        page.screenshot(path="ss-comp-last-page.png")
        with page.expect_download() as download_info:
             page.get_by_role("link", name=" View PDF").click()
        download =  download_info.value
        download.save_as("downloaded_file.pdf")
        page.wait_for_load_state("load")
        page.get_by_role("button", name=" 100192 / 000 / NEFO4081").click()
        page.get_by_role("link", name=" Logout").click()
        page.wait_for_load_state("load")
        return "Automation completed successfully."
    except Exception as e:
        #logger.error(f"Error in process_individual_report_all_steps: {e}")
        return f"Error: {str(e)}"
    finally:
        context.close()
        browser.close()

@app.get("/01")
def run_playwright():
    try:
        with sync_playwright() as playwright:
            result =  do(playwright) 
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)