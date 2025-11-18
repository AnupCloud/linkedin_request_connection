from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Global driver instance
_driver_instance = None


class LinkedInAutomationInput(BaseModel):
    """Input schema for LinkedIn Automation."""
    action: str = Field(description="Action to perform: 'login', 'search', or 'message'")
    email: Optional[str] = Field(default=None, description="LinkedIn email")
    password: Optional[str] = Field(default=None, description="LinkedIn password")
    person_name: Optional[str] = Field(default=None, description="Name of person to search")
    message: Optional[str] = Field(default=None, description="Message to send")


class LinkedInLoginInput(BaseModel):
    """Input schema for LinkedIn Login."""
    email: str = Field(default="", description="Leave empty - credentials are automatically loaded from .env file")
    password: str = Field(default="", description="Leave empty - credentials are automatically loaded from .env file")


class LinkedInSearchInput(BaseModel):
    """Input schema for LinkedIn Search."""
    person_name: str = Field(description="Name of the person to search for")


class LinkedInMessageInput(BaseModel):
    """Input schema for LinkedIn Message."""
    message: str = Field(description="Message to send")


class LinkedInConnectInput(BaseModel):
    """Input schema for LinkedIn Connection Request."""
    note: str = Field(description="Personal note to include with the connection request")


class LinkedInLoginTool(BaseTool):
    name: str = "LinkedIn Login Tool"
    description: str = (
        "Logs into LinkedIn using credentials from environment variables (.env file). "
        "Automatically loads LINKEDIN_EMAIL and LINKEDIN_PASSWORD. "
        "No parameters required - credentials are loaded automatically. "
        "Returns the driver instance for subsequent operations."
    )
    args_schema: Type[BaseModel] = LinkedInLoginInput

    def _run(self, email: str = "", password: str = "") -> str:
        """Execute LinkedIn login."""
        global _driver_instance

        try:
            # Always get credentials from environment variables
            # Ignore any passed parameters that are just placeholder strings
            email = os.getenv("LINKEDIN_EMAIL")
            password = os.getenv("LINKEDIN_PASSWORD")

            if not email or not password:
                return "Error: LinkedIn credentials not found in environment variables. Please check your .env file."

            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Initialize driver
            _driver_instance = webdriver.Chrome(options=chrome_options)

            # Navigate to LinkedIn
            _driver_instance.get("https://www.linkedin.com/login")
            time.sleep(2)

            # Enter credentials
            email_field = WebDriverWait(_driver_instance, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(email)

            password_field = _driver_instance.find_element(By.ID, "password")
            password_field.send_keys(password)

            # Click login button
            login_button = _driver_instance.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()

            # Wait for login to complete
            time.sleep(5)

            # Check if login was successful
            if "feed" in _driver_instance.current_url or "mynetwork" in _driver_instance.current_url:
                return f"Successfully logged into LinkedIn as {email}"
            else:
                return "Login may have failed or requires additional verification"

        except Exception as e:
            if _driver_instance:
                _driver_instance.quit()
                _driver_instance = None
            return f"Error during LinkedIn login: {str(e)}"


class LinkedInSearchTool(BaseTool):
    name: str = "LinkedIn Search Tool"
    description: str = (
        "Searches for a person on LinkedIn and navigates to their profile."
    )
    args_schema: Type[BaseModel] = LinkedInSearchInput

    def _run(self, person_name: str) -> str:
        """Execute LinkedIn search."""
        global _driver_instance

        try:
            if not _driver_instance:
                return "Error: Please login first using LinkedIn Login Tool"

            # Navigate to search
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={person_name.replace(' ', '%20')}"
            print(f"[DEBUG] Searching for: {person_name}")
            print(f"[DEBUG] Search URL: {search_url}")
            _driver_instance.get(search_url)
            time.sleep(5)  # Increased wait time for results to load

            # Check current URL for debugging
            current_url = _driver_instance.current_url
            print(f"[DEBUG] Current URL after search: {current_url}")

            # Wait for search results with multiple selectors
            try:
                # Try different selectors for search results
                selectors = [
                    "li.reusable-search__result-container",
                    "li[class*='search-result']",
                    "div.search-results-container",
                    "ul.reusable-search__entity-result-list"
                ]

                first_result = None
                for selector in selectors:
                    try:
                        print(f"[DEBUG] Trying selector: {selector}")
                        first_result = WebDriverWait(_driver_instance, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        print(f"[DEBUG] Found result with selector: {selector}")
                        break
                    except TimeoutException:
                        continue

                if not first_result:
                    print(f"[DEBUG] No results found for any selector")
                    # Take a screenshot for debugging
                    try:
                        screenshot_path = f"/tmp/linkedin_search_{person_name.replace(' ', '_')}.png"
                        _driver_instance.save_screenshot(screenshot_path)
                        print(f"[DEBUG] Screenshot saved to: {screenshot_path}")
                    except:
                        pass
                    return f"No search results found for '{person_name}'. Please verify the name spelling or try searching on LinkedIn manually first."

                print(f"[INFO] ✓ Found search results for '{person_name}'")
                print(f"[INFO] → Selecting FIRST person from search results...")

                # Find the first profile link - try finding all links and filter for profile links
                print(f"[DEBUG] Looking for profile links in search results...")

                # First, try to find all clickable profile links
                try:
                    # Get all links in the first result
                    all_links = first_result.find_elements(By.TAG_NAME, "a")
                    print(f"[DEBUG] Found {len(all_links)} links in first result")

                    profile_link = None
                    for link in all_links:
                        try:
                            href = link.get_attribute("href")
                            if href and "/in/" in href and "linkedin.com/in/" in href:
                                profile_link = link
                                print(f"[DEBUG] Found profile link: {href}")
                                break
                        except:
                            continue

                    if not profile_link:
                        # Try finding by parent container
                        print(f"[DEBUG] Trying alternative selectors...")
                        link_selectors = [
                            "a.app-aware-link[href*='/in/']",
                            "a[href*='/in/']",
                            ".entity-result__title-text a",
                            "span.entity-result__title-text a",
                            ".entity-result__content a[href*='/in/']"
                        ]

                        for link_sel in link_selectors:
                            try:
                                profile_link = first_result.find_element(By.CSS_SELECTOR, link_sel)
                                if profile_link:
                                    print(f"[DEBUG] Found with selector: {link_sel}")
                                    break
                            except NoSuchElementException:
                                continue

                    if not profile_link:
                        # Take screenshot for debugging
                        try:
                            screenshot_path = f"/tmp/linkedin_search_results_{person_name.replace(' ', '_')}.png"
                            _driver_instance.save_screenshot(screenshot_path)
                            print(f"[DEBUG] Screenshot saved to: {screenshot_path}")
                        except:
                            pass
                        return f"Found search results but couldn't find profile link for '{person_name}'. Screenshot saved for debugging."

                except Exception as e:
                    print(f"[DEBUG] Error finding profile link: {str(e)}")
                    return f"Found search results but couldn't extract profile link for '{person_name}': {str(e)}"

                profile_url = profile_link.get_attribute("href")
                print(f"[INFO] ✓ FIRST result profile URL: {profile_url}")
                print(f"[INFO] → Clicking on this profile...")
                profile_link.click()
                time.sleep(4)
                print(f"[INFO] ✓ Navigated to profile page")

                # Get profile name
                try:
                    name_selectors = [
                        "h1.text-heading-xlarge",
                        "h1[class*='heading']",
                        "h1.inline"
                    ]

                    profile_name = None
                    for name_sel in name_selectors:
                        try:
                            profile_name = WebDriverWait(_driver_instance, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, name_sel))
                            ).text
                            if profile_name:
                                break
                        except:
                            continue

                    if profile_name:
                        print(f"[INFO] ══════════════════════════════════════════")
                        print(f"[INFO] ✓ SELECTED FIRST RESULT: {profile_name}")
                        print(f"[INFO] ✓ Profile URL: {profile_url}")
                        print(f"[INFO] ══════════════════════════════════════════")
                        return f"Found FIRST profile in search results: {profile_name}\nProfile URL: {profile_url}\nThis is the person who will receive your connection request."
                    else:
                        print(f"[DEBUG] Couldn't extract name but on profile")
                        return f"Navigated to profile but couldn't extract name\nProfile URL: {profile_url}"
                except Exception as e:
                    print(f"[DEBUG] Error extracting profile name: {str(e)}")
                    return f"Navigated to profile but couldn't extract name\nProfile URL: {profile_url}"

            except TimeoutException:
                print(f"[DEBUG] Timeout waiting for search results")
                return f"No search results found for '{person_name}'. The profile may not exist or name may be spelled differently."

        except Exception as e:
            print(f"[DEBUG] Error during search: {str(e)}")
            return f"Error during LinkedIn search: {str(e)}"


class LinkedInMessageTool(BaseTool):
    name: str = "LinkedIn Message Tool"
    description: str = (
        "Checks if messaging is available and sends a message on the current LinkedIn profile."
    )
    args_schema: Type[BaseModel] = LinkedInMessageInput

    def _run(self, message: str) -> str:
        """Execute LinkedIn messaging."""
        global _driver_instance

        try:
            if not _driver_instance:
                return "Error: Please login first using LinkedIn Login Tool"

            time.sleep(2)

            # Look for message button
            try:
                # Try different selectors for message button
                message_button = None
                selectors = [
                    "button.pvs-profile-actions__action[aria-label*='Message']",
                    "button[aria-label*='Message']",
                    "a[href*='/messaging/']",
                ]

                for selector in selectors:
                    try:
                        message_button = _driver_instance.find_element(By.CSS_SELECTOR, selector)
                        if message_button:
                            break
                    except NoSuchElementException:
                        continue

                if not message_button:
                    return "Message button not available for this profile. User may not be a connection or messaging may be restricted."

                # Click message button
                message_button.click()
                time.sleep(2)

                # Find message input box
                message_box = WebDriverWait(_driver_instance, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.msg-form__contenteditable"))
                )

                # Type message
                message_box.click()
                message_box.send_keys(message)
                time.sleep(1)

                # Send message
                send_button = _driver_instance.find_element(By.CSS_SELECTOR, "button.msg-form__send-button")
                send_button.click()
                time.sleep(2)

                return f"Successfully sent message: '{message}'"

            except TimeoutException:
                return "Message button found but unable to send message. May require verification or connection request."
            except NoSuchElementException:
                return "Message button not available for this profile."

        except Exception as e:
            return f"Error during LinkedIn messaging: {str(e)}"
        finally:
            # Close browser after all automation tasks are complete
            if _driver_instance:
                time.sleep(3)
                _driver_instance.quit()
                _driver_instance = None


class LinkedInConnectTool(BaseTool):
    name: str = "LinkedIn Connection Request Tool"
    description: str = (
        "Sends a connection request with a personalized note to a LinkedIn profile. "
        "Use this when the person is not yet in your network and you want to connect with them."
    )
    args_schema: Type[BaseModel] = LinkedInConnectInput

    def _run(self, note: str) -> str:
        """Execute LinkedIn connection request with note."""
        global _driver_instance

        try:
            if not _driver_instance:
                return "Error: Please login first using LinkedIn Login Tool"

            time.sleep(3)

            print(f"[DEBUG] Looking for Connect button...")

            # Look for Connect button with comprehensive detection
            try:
                connect_button = None

                # Strategy 1: Try CSS selectors
                selectors = [
                    "button[aria-label*='Connect']",
                    "button.pvs-profile-actions__action[aria-label*='Connect']",
                    "button.artdeco-button--secondary[aria-label*='Connect']",
                    "button[aria-label*='Invite']",
                    "div.pvs-profile-actions button[aria-label*='Connect']",
                ]

                for selector in selectors:
                    try:
                        print(f"[DEBUG] Trying selector: {selector}")
                        connect_button = _driver_instance.find_element(By.CSS_SELECTOR, selector)
                        if connect_button and connect_button.is_displayed():
                            print(f"[DEBUG] ✓ Found Connect button with selector: {selector}")
                            break
                        else:
                            connect_button = None
                    except NoSuchElementException:
                        continue

                # Strategy 2: Find all buttons and search for "Connect" in text
                if not connect_button:
                    print(f"[DEBUG] Trying to find Connect button by text content...")
                    try:
                        all_buttons = _driver_instance.find_elements(By.TAG_NAME, "button")
                        print(f"[DEBUG] Found {len(all_buttons)} total buttons on page")
                        for button in all_buttons:
                            try:
                                button_text = button.text.strip()
                                aria_label = button.get_attribute("aria-label") or ""
                                if ("Connect" in button_text or "Connect" in aria_label) and button.is_displayed():
                                    connect_button = button
                                    print(f"[DEBUG] ✓ Found Connect button by text: '{button_text}' / aria-label: '{aria_label}'")
                                    break
                            except:
                                continue
                    except Exception as e:
                        print(f"[DEBUG] Error searching buttons by text: {str(e)}")

                if not connect_button:
                    # Take screenshot for debugging
                    try:
                        screenshot_path = "/tmp/linkedin_connect_not_found.png"
                        _driver_instance.save_screenshot(screenshot_path)
                        print(f"[DEBUG] Screenshot saved to: {screenshot_path}")
                    except:
                        pass
                    return "Connect button not available. The person may already be a connection, or you may have a pending request."

                print(f"[INFO] ✓ Found Connect button, clicking...")

                # Click connect button
                connect_button.click()
                print(f"[INFO] ✓ Clicked Connect button, waiting for dialog...")
                time.sleep(3)

                # Look for "Add a note" button
                try:
                    print(f"[DEBUG] Looking for 'Add a note' button...")
                    add_note_selectors = [
                        "button[aria-label='Add a note']",
                        "button[aria-label*='Add a note']",
                        "button[aria-label*='note']",
                    ]

                    add_note_button = None
                    for selector in add_note_selectors:
                        try:
                            print(f"[DEBUG] Trying 'Add a note' selector: {selector}")
                            add_note_button = WebDriverWait(_driver_instance, 5).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                            if add_note_button:
                                print(f"[DEBUG] ✓ Found 'Add a note' button with selector: {selector}")
                                break
                        except TimeoutException:
                            continue

                    if add_note_button:
                        add_note_button.click()
                        print(f"[INFO] ✓ Clicked 'Add a note' button")
                        time.sleep(2)

                        # Find the note text area
                        print(f"[DEBUG] Looking for note textarea...")
                        note_textarea = WebDriverWait(_driver_instance, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='message']"))
                        )
                        print(f"[DEBUG] ✓ Found note textarea")

                        # Type the note
                        note_textarea.click()
                        note_textarea.clear()
                        note_textarea.send_keys(note)
                        print(f"[INFO] ✓ Typed personalized note: '{note[:50]}...'")
                        time.sleep(1)

                        # Click Send button
                        print(f"[DEBUG] Looking for Send button...")
                        send_selectors = [
                            "button[aria-label='Send now']",
                            "button[aria-label*='Send']",
                        ]

                        send_button = None
                        for selector in send_selectors:
                            try:
                                send_button = _driver_instance.find_element(By.CSS_SELECTOR, selector)
                                if send_button and send_button.is_displayed():
                                    print(f"[DEBUG] ✓ Found Send button with selector: {selector}")
                                    break
                            except NoSuchElementException:
                                continue

                        if send_button:
                            send_button.click()
                            print(f"[INFO] ✓ Clicked Send button")
                            time.sleep(3)
                            print(f"[INFO] ══════════════════════════════════════════")
                            print(f"[INFO] ✓ CONNECTION REQUEST SENT SUCCESSFULLY!")
                            print(f"[INFO] ✓ Note included: '{note}'")
                            print(f"[INFO] ══════════════════════════════════════════")
                            return f"Successfully sent connection request with note: '{note}'"
                        else:
                            print(f"[DEBUG] Could not find Send button")
                            return "Found note dialog but could not find Send button."

                    else:
                        # If "Add a note" is not available, try to send without note
                        print(f"[DEBUG] 'Add a note' button not found, trying to send without note...")
                        try:
                            send_button = _driver_instance.find_element(By.CSS_SELECTOR, "button[aria-label='Send without a note']")
                            send_button.click()
                            time.sleep(2)
                            print(f"[INFO] ✓ Sent connection request without note option")
                            return f"Sent connection request (note option not available)"
                        except NoSuchElementException:
                            # Try generic Send button
                            try:
                                send_button = _driver_instance.find_element(By.CSS_SELECTOR, "button[aria-label*='Send']")
                                send_button.click()
                                time.sleep(2)
                                print(f"[INFO] ✓ Sent connection request")
                                return f"Sent connection request (attempted with note: '{note}')"
                            except NoSuchElementException:
                                return "Unable to complete connection request. Dialog opened but could not send."

                except Exception as note_error:
                    print(f"[DEBUG] Error in note handling: {str(note_error)}")
                    return f"Connect button clicked but error adding note: {str(note_error)}"

            except NoSuchElementException:
                return "Connect button not found. May already be connected or have a pending request."

        except Exception as e:
            return f"Error during LinkedIn connection request: {str(e)}"