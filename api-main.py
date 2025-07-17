from fastapi import FastAPI, HTTPException, status, Request, Depends
import uvicorn, asyncio
from playwright.async_api import  async_playwright  
from config import USERNAME, PASSWORD, LOGIN_URL, HEADLESS
import logging
import time
import os
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from config_helper import load_settings, update_env

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Playwright Web API ver. 1.3"}

@app.get("/test-company")
async def test_company(
    message_id: str = "00025FTICREVI2025",
    trade_name: str = "PT Prima Tata Solusindo",
    address: str = "Gedung Graha Pena Jawa Pos Lt.5, Jl Raya Kebayoran Lama No.12",
    sub_district: str = "GROGOL UTARA",
    district: str = "KEBAYORAN LAMA",
    postal_code: str = "20146",
    business_number: str = "028822948013000",
    phone: str = "08119931126"
):
    try:
        #async with async_playwright() as playwright:
        #    result = await main_company(playwright) 
        result = await get_company(message_id, trade_name, address, sub_district, district, postal_code, business_number, phone)
        if "error" in result:
            return {"status": "failed", "message": result}
        else:
            return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_company")
async def get_company(
    message_id: str = "00025FTICREVI2025",
    trade_name: str = "PT Prima Tata Solusindo",
    address: str = "Gedung Graha Pena Jawa Pos Lt.5, Jl Raya Kebayoran Lama No.12",
    sub_district: str = "GROGOL UTARA",
    district: str = "KEBAYORAN LAMA",
    postal_code: str = "20146",
    business_number: str = "028822948013000",
    phone: str = "08119931126"
) -> str:
    playwright = None
    browser = None
    context = None
    page = None   
    max_retries = 3
    base_delay = 5
    last_error = None  
    for attempt in range(0, max_retries):

        try:
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(headless=HEADLESS)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(LOGIN_URL)
            await page.wait_for_load_state("load")
            await page.get_by_role("button", name="").click()
            await page.get_by_role("link", name="English").click()

            await page.get_by_role("textbox", name="Username").fill(USERNAME)
            await page.get_by_role("textbox", name="Password").fill(PASSWORD)
            await page.get_by_role("button", name="Login").click()
            
            await page.wait_for_load_state("load")
            await page.get_by_role("link", name="Company").nth(2).click()

            await page.wait_for_load_state("load")
            await page.locator("#CompanyModel_PurposeOfEnquiry").select_option("20")
            await page.locator("#CompanyModel_CompanyDataModel_MessageID").fill(message_id)
            await page.locator("#CompanyModel_CompanyDataModel_TradeName").fill(trade_name)
            await page.get_by_role("textbox", name="FIELD 'ADDRESS' LENGTH IS NOT").fill(address)
            await page.get_by_role("textbox", name="FIELD 'SUB DISTRICT' IS").fill(sub_district)
            await page.get_by_role("textbox", name="FIELD 'DISTRICT' IS MANDATORY").fill(district)
            await page.locator("#CompanyModel_AddressDataModel_City").select_option("0394")
            await page.get_by_role("textbox", name="FIELD 'POSTAL CODE' IS").fill(postal_code)
            await page.locator("#CompanyModel_AddressDataModel_Country").select_option("ID")
            await page.locator("#CompanyModel_IdentificationCodeModel_BusniessNumber").fill(business_number)
            await page.get_by_role("textbox", name="AT LEAST ONE BETWEEN 'PHONE").fill(phone)

            await page.wait_for_load_state("load")
            await page.get_by_text("Next").click()

            await page.wait_for_load_state("load")
            await page.locator("#ContractModel_IndividualRole").select_option("B")
            await page.locator("#operationCombo").select_option("[[N99,F01],F01]")
            await page.locator("#ContractModel_ContractDataModelCredit_ApplicationAmount").fill("100000000")
            await page.get_by_text("Submit").click()

            await page.wait_for_load_state("load")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            report_file_name = f"{message_id}_company_{timestamp}.html"
            html_content = await page.content()
            with open(report_file_name, "w", encoding="utf-8") as f:
                f.write(html_content)

            await context.close()
            await browser.close()
            await playwright.stop()
            
            logger.info(f"Attempt {attempt+1} succeeded")
            return f"Clik Company RPA completed successfully on {attempt+1} attempt."

        except Exception as e:
            last_error = e
            logger.error(f"Attempt {attempt+1} failed: {str(e)}")
            
            if page:
                await page.screenshot(path=f"ss-comp-error-attempt{attempt+1}.png")
            if context:
                await context.close()
            if browser:
                await browser.close()
            if playwright:
                await playwright.stop()
            
            if attempt < max_retries:
                delay = base_delay * (2 ** (attempt - 1))
                logger.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
    
    # If all attempts failed
    logger.error("All retry attempts on Company report failed")
    raise HTTPException(
        status_code=500, 
        detail=f"Company report failed after {max_retries} attempts. Last error: {str(last_error)}"
    )


@app.get("/get_individual")
async def get_individual(
    message_id: str = "00026FTICREVI2026",
    name: str = "Tri Wahyudin",
    birth_date: str = "1977/11/26",
    gender: str = "L",
    address: str = "JL RAYA PKP GRAHA ARJUNA NO G",
    sub_district: str = "KELAPA DUA WETAN",
    district: str = "CIRACAS",
    city: str = "0395",
    postal_code: str = "13730",
    country: str = "ID",
    identity_type: str = "1",
    id_number: str = "3276052611770004",
    phone_number: str = "08119931126"
) -> str:
    playwright = None
    browser = None
    context = None
    page = None   
    max_retries = 3
    base_delay = 5 
    last_error = None
    for attempt in range(0, max_retries):
        try:
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(headless=HEADLESS)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(LOGIN_URL)
            await page.wait_for_load_state("load")
            await page.get_by_role("button", name="").click()
            await page.get_by_role("link", name="English").click()

            await page.get_by_role("textbox", name="Username").fill(USERNAME)
            await page.get_by_role("textbox", name="Password").fill(PASSWORD)
            await page.get_by_role("button", name="Login").click()

            await page.wait_for_load_state("load")
            await page.get_by_role("link", name="Individual").first.click()

            await page.wait_for_load_state("load")
            await page.locator("#IndividualModel_PurposeOfEnquiry").select_option("20")
            await page.locator("#IndividualModel_IndividualDataModel_MessageID").fill(message_id)
            await page.locator("#IndividualModel_IndividualDataModel_NameAsId").fill(name)
            await page.get_by_role("textbox", name="YYYY/MM/DD").fill(birth_date)
            await page.get_by_role("textbox", name="YYYY/MM/DD").press("Enter")
            await page.locator("#IndividualModel_IndividualDataModel_GenderCode").select_option(gender)
            await page.get_by_role("textbox", name="FIELD 'ADDRESS' LENGTH IS NOT").fill(address)
            await page.get_by_role("textbox", name="FIELD 'SUB DISTRICT' IS").fill(sub_district)
            await page.get_by_role("textbox", name="FIELD 'DISTRICT' IS MANDATORY").fill(district)
            await page.locator("#IndividualModel_AddressDataModel_City").select_option(city)
            await page.get_by_role("textbox", name="FIELD 'POSTAL CODE' IS").fill(postal_code)
            await page.locator("#IndividualModel_AddressDataModel_Country").select_option(country)
            await page.locator("#IndividualModel_IdentificationCodeDataModel_Type").select_option(identity_type)
            await page.locator("#IndividualModel_IdentificationCodeDataModel_Id").fill(id_number)
            await page.locator("#IndividualModel_ContactDataModel_PhoneNumber").fill(phone_number)
            await page.get_by_text("Next").click()

            await page.wait_for_load_state("load")
            await page.locator("#ContractModel_IndividualRole").select_option("B")
            await page.locator("#operationCombo").select_option("[[P99,F01],F01]")
            await page.locator("#ContractModel_ContractDataModelCredit_ApplicationAmount").fill("100000000")
            await page.get_by_text("Submit").click()

            await page.wait_for_load_state("load")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            report_file_name = f"{message_id}_individual_{timestamp}.html"
            html_content = await page.content()
            with open(report_file_name, "w", encoding="utf-8") as f:
                f.write(html_content)

            await context.close()
            await browser.close()
            await playwright.stop()
            await context.close()
            await browser.close()
            await playwright.stop()
            
            logger.info(f"Attempt {attempt+1} succeeded")
            return f"Clik Individual RPA completed successfully on {attempt+1} attempt."

        except Exception as e:
            last_error = e
            logger.error(f"Attempt {attempt+1} failed: {str(e)}")
            
            if page:
                await page.screenshot(path=f"ss-indv-error-attempt{attempt+1}.png")
            if context:
                await context.close()
            if browser:
                await browser.close()
            if playwright:
                await playwright.stop()
            
            if attempt < max_retries:
                delay = base_delay * (2 ** (attempt - 1))
                logger.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
    
    # If all attempts failed
    logger.error("All retry attempts on Individual report failed")
    raise HTTPException(
        status_code=500, 
        detail=f"Individual report failed after {max_retries} attempts. Last error: {str(last_error)}"
    )
# ---= Experimental section =---
# ---  API-Key Security ---
API_KEY = "supersecret123"
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

def require_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key"
        )

# --- Schema for Validation ---
class ConfigModel(BaseModel):
    LOGIN_URL: str
    USERNAME: str
    PASSWORD: str
    BASE_URL: str
    HEADLESS: bool

# --- FastAPI App Setup ---
#app.mount("/", StaticFiles(directory="slash"), name="root")
templates = Jinja2Templates(directory="templates")

@app.get(
    "/config",
    response_model=ConfigModel,
    #dependencies=[Depends(require_api_key)]
)
def get_config():
    return load_settings()

@app.put(
    "/config",
    response_model=ConfigModel,
    #dependencies=[Depends(require_api_key)]
)
def put_config(cfg: ConfigModel):
    update_env(cfg.dict())
    return cfg

@app.get(
    "/admin"
)
def admin_page(request: Request):
    cfg = load_settings()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "config": cfg
    })

if __name__ == "__main__":
    uvicorn.run(
        "api-main:app",        
        host="0.0.0.0",
        port=8000,
        reload=True
    )
