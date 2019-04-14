# pybrowser

For documentation, refer [here](https://pybrowser.readthedocs.io/en/latest/)

## Release Notes:
## ==============
**0.1.0**
*   Changes
    ``Please note some key changes with regards to properties changing to methods``
    *   Methods which were properties in initial release are now method calls. Below is the impacted list.
        In Browser,
            `<Browser.refresh()>`
            `<Browser.back()>`
            `<Browser.forward()>`
            `<Browser.maximize_window()>`
            `<Browser.minimize_window()>`
            `<Browser.fullscreen_window()>`
            `<Browser.delete_all_cookies()>`
            `<Browser.close()>`

        In Action (used by all elements),
            `<Action.refresh()>`
            `<Action.highlight()>`
            `<Action.double_click()>`
            `<Action.move_to_element()>`

        Specific elements also,
            `<Checkbox.check()>`
            `<Checkbox.uncheck()>`
            `<Radio.select()>`
            `<Radio.unselect()>`
            `<Input.clear()>`
    
    *   Browser class init method now has more options,
            `<firefox_binary_path>`
            `<firefox_profile_path>`
            `<http_proxy>`
            `<driver_path>`
    
    *   Select element has below method changes,
        `<Select.options(get="text")>` method has been split to multiple properties to keep it simple,
            `<Select.options_text>`
            `<Select.options_value>`
            `<Select.options_element>`
        Similar change has been done for `<Select.all_selected_options(get="text")>`,
            `<Select.all_selected_options_text>`
            `<Select.all_selected_options_value>`
            `<Select.all_selected_options_element>`

    *   Changes in some env options.
        Removed below options as they don't have sense. Either you provide complete driver download url or provide version
        so that the API tries to download,
            `<CHROME_FILENAME>`
            `<IE_FILENAME>`
            `<CHROMEDRIVER_DEFAULT_VERSION>`
        
        Added below for Firefox support,
            `<FIREFOX_HOME_URL>`
            `<FIREFOX_DOWNLOAD_URL>`
            `<FIREFOXDRIVER_VERSION>`
    
    *   Refactoring (non functional) in code and tests. Lot more testing needed still :-\

*   New features
    *   Support for Firefox !

**0.0.1**
Very first release !