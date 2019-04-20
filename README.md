# pybrowser

For documentation, refer [here](https://pybrowser.readthedocs.io/en/latest/)

## Release Notes:

**0.2.0**
---------

*   **Changes**

    *   Changes in underlying `Browser.requests_session` object,

        *   `requests_session.result` has been removed. There is just `requests_session.response` which is a blocking call (in case `asynch` flag is set). Also note, `requests_session.is_request_done` is still available to see if request is complete of not. There are no changes to other properties and are blocking in case of asynchronous call.

        *   `requests_session.content()` method with options for bytes and text has been changed to properties, just like in underlying requests. That is now you call, `requests_session.content` for bytes and `requests_session.text` for text.

        *   In context of above changes, `Browser` object also has below changes,

            *   `Browser.get` and `Browser.post` now returns `requests_session` object (used to be `requests_session.response`).
            *   `Browser.content()` has been changed to properties. That is now you call, `Browser.content` for bytes and `Browser.text` for text.

*   **New features**

    *   Support for remote url. Please note this requires [Selenium Grid](https://www.seleniumhq.org/docs/07_selenium_grid.jsp) to be setup explicitly. Once done use the URL here.

    * Flags for Opera browser (`Browser.OPERA`). Webdriver executable needs to be present in `driver_path`.
    Please note `EDGE` and `SAFARI` are also supported the same way. That is, webdriver isn't automatically downloaded, instead path needs to be provided.

**0.1.0**
---------

*   **Changes**

    **Please note some key changes with regards to properties changing to methods**.

    *   Methods which were properties in initial release are now method calls. Below is the impacted list.
        
        In Browser,

        *   `Browser.refresh()`
        *   `Browser.back()`
        *   `Browser.forward()`
        *   `Browser.maximize_window()`
        *   `Browser.minimize_window()`
        *   `Browser.fullscreen_window()`
        *   `Browser.delete_all_cookies()`
        *   `Browser.close()`

        In Action (used by all elements),

        *   `Action.refresh()`
        *   `Action.highlight()`
        *   `Action.double_click()`
        *   `Action.move_to_element()`

        Specific elements also,

        *   `Checkbox.check()`
        *   `Checkbox.uncheck()`
        *   `Radio.select()`
        *   `Radio.unselect()`
        *   `Input.clear()`
    
    *   Browser class `__init__` method now has more options,

        *   `firefox_binary_path`
        *   `firefox_profile_path`
        *   `http_proxy`
        *   `driver_path`
    
    *   Select element has below method changes,

        `Select.options(get="text")` method has been split to multiple properties to keep it simple,

        *   `Select.options_text`
        *   `Select.options_value`
        *   `Select.options_element`

        Similar change has been done for `Select.all_selected_options(get="text")`,

        *   `Select.all_selected_options_text`
        *   `Select.all_selected_options_value`
        *   `Select.all_selected_options_element`
    
    *   File element changes,

        Below enhancements have been made to download feature,

        *   Added more parameters - 

            *   `unzip` - Set this flag to unzip file. Default is `False`
            *   `del_zipfile` - Set this flag to delete zip file after it has been unzipped. Default is `False`
            *   `add_to_ospath` - Set this flag to add directory to `PATH`. Default is `False`
        
        *   New properties - 

            As you might already know, download happens in background (asynchronous) by default and can of course be changed with `asynch`. To check if download was successful, below properties are available,

            *   `is_download_complete` - `True` or `False`
            *   `downloaded_files` - list of downloaded files
    
    *   HTML links method has below method changes,

        This is the one you would invoke via Browser as `Browser.html().elements.link()`.

        *   Added more parameters - 

            *   `images` - You can filter out images. Default is `False` that means to include `images`, you will need to set this to `True`
            *   `name_length_limit` - This limits the length of name of the url. Default is 60
        
        *   Change in return type. Before this change, return type was a list of types (name, url). This has been changed to list of [named_tuples](https://docs.python.org/3.7/library/collections.html#collections.namedtuple) of form `('Link', ['name', 'url'])`

    *   Changes in some env options.

        Removed below options as they don't have sense. Either you provide complete driver download url or provide version
        so that the API tries to download,

        *   `CHROME_FILENAME`
        *   `IE_FILENAME`
        *   `CHROMEDRIVER_DEFAULT_VERSION`
        
        Added below for Firefox support,

        *   `FIREFOX_HOME_URL`
        *   `FIREFOX_DOWNLOAD_URL`
        *   `FIREFOXDRIVER_VERSION`
    
    *   Refactoring (non functional) in code and tests. Lot more testing needed still :-\

*   **New features**

    *   Support for Firefox !

**0.0.1**
---------

*   Very first release !