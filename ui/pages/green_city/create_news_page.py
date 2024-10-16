from typing import Optional

from playwright.sync_api import Page

from ui.pages.green_city.green_city_base_page import GreenCityBasePage
from ui.enum.news_tags import NewsTags
import os
import allure

from ui.pages.green_city.news_preview_page import NewsPreviewPage


class CreateNewsPage(GreenCityBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.news_title = self.page.locator("//textarea[@formcontrolname='title']")
        self.news_content = self.page.locator("//div[@class='ql-editor ql-blank']")
        self.source_link_field = self.page.locator("//div[contains(@class, 'source-block')]//label/input")
        self.tags_button = self.page.locator("//app-tags-select//button/a")
        self.news_preview_button = self.page.locator("//button[contains(@class, 'secondary-global-button')]")
        self.news_publish_button = self.page.locator("//div[contains(@class, 'submit-buttons')]//button[@type='submit']")
        self.news_photo = self.page.locator("//div[@class='text-wrapper']")
        self.news_is_loading_message = self.page.locator("(//div[@class='container'])[2]")
        self.close_tag_button = self.page.locator("//div[contains(@class, 'global-tag-close-icon')]")
        self.add_img_link = self.page.locator("//div[contains(@class, 'dropzone')]//span")
        self.submit_img_button = self.page.locator("//div[contains(@class, 'cropper-buttons')]//button[2]")

    @allure.step("Select the tag {tag}")
    def select_single_tag(self, tag: NewsTags, language_code: str):
        tag_text = tag.get_text(language_code)
        tag_button = self.page.get_by_role("button", name=tag_text).locator("a")
        tag_button.click()

    @allure.step("Fill the Create News form with the title: {title}, content: {content}, and the list of tags: {tags}")
    def fill_the_news_form(self, title: str, tags: list[NewsTags], content: str, language: str):
        self.news_title.fill(title)
        for tag in tags:
            self.select_single_tag(tag, language)
        self.news_content.fill(content)
        return self

    @allure.step("Fill the source link field with {link}")
    def enter_source_link(self, link: str):
        self.source_link_field.fill(link)
        return self

    @allure.step("Select the tags: {tags}")
    def select_tags(self, tags: list[NewsTags], language_code: str):
        for tag in tags:
            self.select_single_tag(tag, language_code)
        return self

    @allure.step("Unselect the tags: {tags}")
    def unselect_tags(self, tags: list[NewsTags], language_code):
        for tag in tags:
            self.unselect_single_tag(tag, language_code)
        return self


    @allure.step("Unselect the tag: {tag}")
    def unselect_single_tag(self, tag: NewsTags, language_code: str):
        tag_text = tag.get_text(language_code)

        for tag_button in self.tags_button.all():
            if tag_button.text_content().strip().lower() == tag_text.lower():
                tag_button.locator(self.close_tag_button).click()
                break

        return self

    @allure.step("Get the background color of the {tag} button")
    def get_tag_button_background_color(self, tag: NewsTags) -> Optional[str]:
        tag_text_en = tag.get_text("en")
        tag_text_ua = tag.get_text("ua")

        for tag_button in self.tags_button.all():
            button_text = tag_button.text_content().strip()

            if button_text.lower() == tag_text_en.lower() or button_text.lower() == tag_text_ua.lower():
                return tag_button.evaluate("element => getComputedStyle(element).backgroundColor")

        return None

    @allure.step("Click the newsPublishButton")
    def click_publish_button(self):
        self.page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        self.news_publish_button.click()
        from ui.pages.green_city.news_page import NewsPage

        return NewsPage(self.page)

    @allure.step("Click the newsPreviewButton")
    def click_preview_button(self):
        self.news_preview_button.click()
        return NewsPreviewPage(self.page)

    @allure.step("Verify if the newsPreviewButton is enabled")
    def news_preview_button_is_enabled(self) -> bool:
        return self.news_preview_button.is_enabled()

    @allure.step("Verify if the newsPublishButton is enabled")
    def news_publish_button_is_enabled(self) -> bool:
        return self.news_publish_button.is_enabled()

    @allure.step("Check if the tag {tag} is selected")
    def is_tag_selected(self, tag_button) -> bool:
        class_attribute = tag_button.get_attribute("class")
        return "global-tag-clicked" in class_attribute

    @allure.step("Get all selected tag")
    def get_selected_tags(self) -> list:
        selected_tags = []

        for tag_button in self.tags_button.all():
            if self.is_tag_selected(tag_button):
                selected_tags.append(tag_button)

        return selected_tags

    @allure.step("Get news title text")
    def get_title_text(self) -> str:
        return self.news_title.get_attribute("value")

    @allure.step("Get news loading message text")
    def get_news_loading_message(self) -> str:
        return self.news_is_loading_message.text_content()

    @allure.step("Get news content text")
    def get_content_text(self) -> str:
        editor = self.page.locator("quill-editor .ql-editor")

        return editor.evaluate("element => element.innerText")

    @allure.step("Check if the title field is displayed")
    def is_title_field_appeared(self) -> bool:
        return self.news_title.is_visible()

    @allure.step("Check if the content field is displayed")
    def is_content_field_appeared(self) -> bool:
        return self.news_content.is_visible()

    @allure.step("Check if the source field is displayed")
    def is_source_field_appeared(self) -> bool:
        return self.source_link_field.is_visible()

    @allure.step("Check if the photo field is displayed")
    def is_photo_field_appeared(self) -> bool:
        return self.news_photo.is_visible()

    @allure.step("Upload an image from the path {path}")
    def add_image(self, path: str):
        try:
            self.page.set_input_files("input[type='file']", path)
        except Exception as e:
            print(f"Error uploading file: {e}")

        self.submit_img_button.click()

        return self
