import asyncio
import os

from browser_use.agent.service import Agent
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.service import Controller
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr, BaseModel


class CheckoutResult(BaseModel):
    login_status: str
    cart_status: str
    checkout_status: str
    total_update_status: str
    delivery_location_status: str
    confirmation_message: str


controller = Controller(output_model=CheckoutResult)

@controller.action('Get Attribute and URL of the page')
async def get_attr_url(browser: BrowserContext):
    page = await browser.get_current_page()
    current_url = page.url
    attr = page.get_by_text("Shop Name").get_attribute("class")
    print(attr)
    return ActionResult(extracted_content=f'current url is {current_url} and attr is {attr}')


async def site_validation():
    os.environ["GEMINI_API_KEY"] = "AIzaSyCk5E5WMv-Yyb9ri57KrwmejwUahTdl_Eg"
    task = (
        'Important: I am a UI Automation Tester validating the tasks '
        'Open website https://rahulshettyacademy.com/loginpagePractise/ '
        'Login with username and password, login details are available in the same page '
        'Get Attribute and URL of the page'
        'After login, select first 2 products and add them to the cart '
        'Then checkout and store the total value you see in screen '
        'Increase the quantity of any product and check if the value updates accordingly '
        'checkout and select country '
        'verify thankyou message is displayed'
    )
    api_key = os.environ["GEMINI_API_KEY"]
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp',
                                 api_key=SecretStr(api_key))
    agent = Agent(task=task, llm=llm, use_vision=True, controller=controller)
    history = await agent.run()
    history.save_to_file('agentresults.json')
    test_result = history.final_result()
    print(test_result)
    assert test_result.confirmation_message == "Unknown"


async def site_validation2():
    os.environ["GEMINI_API_KEY"] = "AIzaSyCk5E5WMv-Yyb9ri57KrwmejwUahTdl_Eg"
    task = (
        'Important: I am a UI Automation Tester validating the tasks '
        'Open website https://rahulshettyacademy.com/client/ '
        'Login with username and password, login details are email akhtarsameer743@gmail.com and password is Sameerking01! '
        'After login, add the first 2 products to the cart '
        'Then go to cart from header and store the total value you see in screen '
        'Click checkout and select country India '
        'verify thankyou message is displayed'
    )
    api_key = os.environ["GEMINI_API_KEY"]
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp',
                                 api_key=SecretStr(api_key))
    agent = Agent(task, llm, use_vision=True)
    history = await agent.run()
    test_result = history.final_result()
    print(test_result)


asyncio.run(site_validation())
