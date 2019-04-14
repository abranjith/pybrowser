.. pybrowser documentation master file, created by
   sphinx-quickstart on Sat Mar 23 16:21:35 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**Welcome to pybrowser's documentation**
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. warning:: Please note that if you are switching from previous version (``0.0.1``) to latest (``0.1.0``), there have been some significant changes and also some new features. Refer release notes in `github <https://github.com/abranjith/pybrowser/blob/master/README.md>`_ to know more before upgrading.

**About the project**
*********************
**pybrowser** is an attempt to simplify browser automation designed keeping end user in mind. Here 
is an example of usage,

.. code-block:: python

    from pybrowser import Browser 
    with Browser(browser_name=Browser.CHROME) as b:
        b.goto("https://www.google.com/")
        b.input("name:=q").enter("news")
        b.button("name:=btnK").click()
        screenshot_path = b.take_screenshot()
        print(b.html().elements.links())

**Why another browser automation API ?**
****************************************
You might be wondering, there are already enough automation APIs / libraries in the market, why another one ?
Well, as a starter, ``pybrowser`` isn't really a library per say, it is merely a toolkit that is an abstraction 
around the well known `Selenium <https://selenium-python.readthedocs.io/>`_ and `Requests <http://docs.python-requests.org/en/master/>`_ 
libraries in python. That means, you are not "forced" to do things in a certain way in ``pybrowser`` as done by other libraries.
Ruby's `watir <http://watir.com/>`_ is the main source of inspiration behind some of the design decissions, but ``pybrowser`` is
much simpler in terms of design as well as usage ! It is also lighweight and doesn't add too much overhead when it comes to abstraction. 

**Features**
************
*   Browser as an object with simple interface to interact with webpage elements
*   Exposes specific HTML elements and corresponding functionalities
*   Special interface to submit HTML forms
*   Cached element attributes
*   Takes care of downloading corresponding browser drivers, adding to the path and other such overheads
*   In built support for handling page/element wait times, staleness of elements and other such issues due to dynamic nature of webpages
*   Access to response code and header information
*   Ability to run browser in headless/incognito/with proxy and all the good stuff
*   Non browser mode support to directly deal with HTML pages & HTTP methods
*   HTML rendering support
*   Default exception handler
*   Uses Selenium and Requests under the hood

**Installation**
----------------
**pybrowser** is not in pypi (the cheeseshop!) yet. 

If you use `pipenv <https://pipenv.readthedocs.io/en/latest/>`_ , it can be installed with below command,

``pipenv install -e git+https://github.com/abranjith/pybrowser.git#egg=pybrowser``

With pip,

``pip install git+https://github.com/abranjith/pybrowser#egg=pybrowser``

`Virtualenv <https://docs.python.org/3/library/venv.html>`_ is highly recommended. Note that, if you are using pipenv, it takes care
of creating virtualenv for you.
Feel free to clone/ fork and play around.

**Requirements**
----------------
*   python 3.7+
*   selenium
*   requests
*   pyppeteer
*   pyquery

Note: Although, I have mentioned as python 3.7 or above, you should be able to get it to run with 3.6 also,
but not prior to that. For versions of other packages refer Pipfile or requirements file

**Detailed guide**
******************

**Browser object**
------------------
Browser is the main object that needs to be instantiated for further usage. Here are some examples,
To use as a typical browser,

.. code-block:: python
    
    #currently supports - Browser.CHROME, Browser.IE and Browser.FIREFOX, 
    #although Chrome is highly recommended
    browser = Browser(browser_name=Browser.CHROME)

Browser supports multiple options as explained below,

*   browser_name - name of the browser such as Browser.IE, Browser.CHROME etc
*   incognito - when set to True, will start browser in incognito mode
*   headless - when set to True, will start browser in headless mode (you won't see the GUI)
*   browser_options - dict of options that you would provide to webdriver of corresponding browser
*   http_proxy - proxy url to use before starting browser
*   screenshot_on_exception - when set to True, takes screenshot when an exception occurs in webdriver
*   wait_time - wait time in seconds to be used in finding elements etc
*   driver_path - If you already have drivers downloaded, just provide the path (directory and not file)
*   firefox_binary_path - Applicable only for firefox. If not present, default firefox in system is used
*   firefox_profile_path - Applicable only for firefox. If not present, default firefox profile is used

Below sections explain the functionalities exposed by Browser.

**As a Web Browser**
--------------------
.. warning::  Please note using any webbrowser requires corresponding webdriver to be present. So if path to one is not provided via ``driver_path``, it will be downloaded from the web

One of the key functionality provided by Browser object is access to your favorite browser as mentioned above. 
You can automate pretty much all of the activities you can do with you browser plus much more. Here are some examples,

*   **Navigation**

    Navigate just like how you would do in a regular browser.

    .. code-block:: python

        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("http://url")
            b.refresh()
            b.back()
            b.forward()

*   **Access to important properties**

    Access various properties of the browser/page like current url, page title, cookies, response data etc.

    .. code-block:: python

        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("http://url")
            #underlying selenium webdriver object
            d = b.driver
            u = b.url
            t = b.title
            c = b.cookies
            rc = b.response_code
            rh = b.response_headers
            re = b.response_encoding
            #content in bytes
            binary_content = b.content(raw=True)
            #content in text
            text_content = b.content(raw=False)

*   **More advanced actions on browser**

    You can perform a bunch of actions with the browser apart from accessing properties and general navigation.

    *   **Change driver**

        If you don't like the underlying selenium webdriver, provide your own

        .. code-block:: python

            b = Browser(browser_name=Browser.CHROME)
            b.driver = your_custom_driver
    
    *   **Change window size**

        .. code-block:: python

            b = Browser(browser_name=Browser.CHROME)
            b.goto("http://url")
            b.maximize_window()
            b.minimize_window()
            b.fullscreen_window()

    *   **Switch to (from Selenium)**

        You can switch to some other window, alert, frame etc. For more refer Selenium documentation `here <https://selenium-python.readthedocs.io/navigating.html/>`_

        .. code-block:: python

            b = Browser(browser_name=Browser.CHROME)
            b.goto("http://url")
            b.switch_to.alert
            b.switch_to.default_content()
            b.switch_to.frame('frame_name')
            b.switch_to.window('main')
    
    *   **Cookies**

        Add / delete/ get cookies

        .. code-block:: python

            b = Browser(browser_name=Browser.CHROME)
            b.goto("http://url")
            print(b.cookies)
            b.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/', 'secure':True})
            b.delete_cookie('name')
            b.delete_all_cookies()
    
    *   **JSON**

        If the response is JSON, get json.

        .. code-block:: python

            b = Browser(browser_name=Browser.CHROME)
            b.goto("http://url")
            print(b.json)

    *   **HTML**

        Get hold of HTML and do more with it. More on this in below section

        .. code-block:: python

            b = Browser(browser_name=Browser.CHROME)
            b.goto("http://url")
            print(b.html())
    
    *   **Underlying requests session**

        Requests is an awesome python library for anything HTTP. More on that `requests-session <http://docs.python-requests.org/en/master/user/advanced/#session-objects>`_

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                session = b.requests_session
    
    *   **Take screenshot**

        You will get saved path in response.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("http://url")
                #guesses path
                p = b.take_screenshot()
                #you can provide filename
                p = b.take_screenshot(filename='filename.png')
                #complete path without filename
                p = b.take_screenshot(filename='/path/to/dir')
                #complete path with filename
                p = b.take_screenshot(filename='/path/to/dir/filename.png')
    
    *   **Execute javascript on browser**

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("http://url")
                b.execute_script("valid javascript for browser")
    
    *   **Close (ofcourse)**

        Closes all underlying sessions. Please note you **do not** have to call this explicitly if you are using context manager !

        .. code-block:: python

            #with context manager no need to call close explicitly. Close is 
            #called automatically  (**recommended**)  
            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("http://url")
            #in this case, you will need to call explicitly
            b = Browser(browser_name=Browser.CHROME)
            b.goto("http://url")
            b.close()
            
*   **Work with page elements**

    In a web page, access various elements and perform actions on them. Here are the various elements available,

    *   **Input**

        Represents any input element such as text, textarea, input type text etc where user can enter some text.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("https://the-internet.herokuapp.com/login")
                b.input("id:=username").enter("someuser")
                b.input("id:=password").clear()
    
    *   **Button**

        Represents any button element such as button, input type button.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("https://the-internet.herokuapp.com/login")
                b.input("username").enter("someuser")
                b.button("xpath:=//*[@id='login']/button").click()
    
    *   **Link**

        Represents any element with a href (typically link to another resource).

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("https://the-internet.herokuapp.com")
                u = b.link("xpath:=//*[@id='content']/ul/li[14]/a").url
    
    *   **Radio**

        Represents a radio button.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("https://www.w3schools.com/php/php_form_complete.asp")
                radio = b.radio("xpath:=/html/body/form//input[@value='female']")
                print(radio.is_displayed)
                print(radio.is_selected)
                radio.select()
                radio.unselect()  #if there is such a thing

    *   **Checkbox**

        Represents a checkbox.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("https://the-internet.herokuapp.com/checkboxes")
                check_box = b.checkbox("xpath:=//*[@id='checkboxes']/input[1]")
                print(check_box.is_checked)
                check_box.check()
                check_box.uncheck()
    
    *   **Select**

        Represents any dropdown with one or many options to select from.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("https://the-internet.herokuapp.com/checkboxes")
                dropdown = b.select("id:=dropdown")
                print(dropdown.options_text)
                print(dropdown.options_value)
                print(dropdown.options_element)
                dropdown.select_by_indices(0)
                dropdown.select_by_visible_texts("Option 1")
                print(dropdown.all_selected_options_text)
                print(dropdown.all_selected_options_value)
                print(dropdown.all_selected_options_element)
                dropdown.deselect_all()
                #... and so on
    
    *   **File**

        Represents a file element which is typically used to upload or download files.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("https://the-internet.herokuapp.com/download")
                fd = b.file("xpath:=//*[@id='content']/div/a[1]")
                fd.download(directory='/to/dir/')
                while not fd.is_download_complete:
                    time.sleep(1)
                print(fd.downloaded_files)
                b.goto("https://the-internet.herokuapp.com/upload")
                b.file("id:=file-upload").upload(filename='/path/to/valid/file')
        
        A note about the download and upload methods -

        ``download`` accepts below parameters,
            *   ``directory`` - where the file gets downloaded. Default is user home
            *   ``as_filename`` - file name for the downloaded file. Default is derived based on url
            *   ``asynch`` - Default is True that means file is downloaded in the background (asynchronous)
            *   ``unzip`` - Default is False. Set to True to unzip downloaded files 
            *   ``del_zipfile`` - Default is False. Set to True to delete zip file after unzipping
            *   ``add_to_ospath`` - Default is False. Set to True to add directory to PATH

        ``download`` also provides below properties to check if download was complete (useful when asynch is True),
            *   ``is_download_complete`` - True or False
            *   ``downloaded_files`` - list of downloaded files

        ``upload`` accepts below parameters,
            *   ``filename`` - has to be a complete path to valid file

    *   **Form**

        Represents a HTML form. Please note special interface and method fill_and_submit_form.

        .. code-block:: python

            form_data = [("id:=username", "tomsmith"), ("id:=password", "SuperSecretPassword!")]
            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("https://the-internet.herokuapp.com/login")
                b.form("id:=login").fill_and_submit_form(form_data)
    
    *   **Element**

        Represents any element which doesn't belong to any of the categories above

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("https://the-internet.herokuapp.com/add_remove_elements/")
                t = b.element("xpath:=//*[@id='content']/h3").text
                print(t)

*   **Locator format**

    You might have already observed a rather peculiar choice for providing locator which is of the form,
    ``locator_type:=locator_value``
    
    ``locator_type`` is any of the Selenium allowed valid By types which are,
    ``ID``, ``NAME``, ``XPATH``, ``LINK_TEXT``, ``PARTIAL_LINK_TEXT``, ``TAG_NAME``, ``CSS_SELECTOR``, ``CLASS_NAME``
    
    Note that these are case insensitive. That is ``name:=some_name`` and ``NAME:=some_name`` are one and the same.

    ``locator_value`` on the other hand is the correspodning value for ``locator_type`` used. 
    ``:=`` is the delimiter used. This has been done instead of just using ``=`` to avoid confusion 
    that might arrive when ``=`` is part of your locator_value.

    Also note, if the ``locator_type`` is ``ID`` or ``NAME``, you can skip the ``locator_type`` and jsut provide ``locator_value``.
    For eg, ``b.element("some_id")`` is totally valid
    Although ``locator_type:=locator_value`` is the recommended syntax.


*   **Common actions on elements**

    Even though above section describes most of the actions, below is a consolidation of some common ones.
    These are common, which means these can be applied on any element.

    .. code-block:: python

        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("http://url")
            e = b.element("id:=element")
            e.click()
            #typically used in forms
            e.submit()
            #just waits for time in seconds 
            e.wait(wait_time=10)
            #physically move to the element 
            e.move_to_element()
            #highlights the element, try this out !   
            e.highlight()
            e.double_click()
            #drag element e and drop at element represented by to_locator
            e.drag_and_drop_at(to_locator="id:=to_element")
            #drag element e and drop at another element     
            e.drag_and_drop_at(to_element=other_element)

*   **Access various properties of page elements**

    Once you identify an element per above bullet point, you can access various properties of the element such as tag_name, id etc. Below are some examples.

    .. code-block:: python

        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://the-internet.herokuapp.com/login")
            ele = b.input("id:=username")
            ele.enter("some_user")
            print(ele.text)
            print(ele.tag_name)
            print(ele.id)
            print(ele.name)
            print(ele.type)
            #basically a list representing all css classess if any
            print(ele.css_classes)
            print(ele.value)
            #href in case it's a link 
            print(ele.href)

*   **Non-HTML properties of page elements**

    Apart from the HTML properties there are some properties which essentially represent meta data around the element such as below.

    .. code-block:: python

        with Browser(browser_name=Browser.CHROME) as b:
            b.goto("https://the-internet.herokuapp.com/login")
            ele = b.input("id:=username")
            print(ele.is_found)
            print(ele.is_displayed)
            #alias to is_displayed
            print(ele.is_visible)
            print(ele.is_enabled)
            #checks if the element has gone stale after finding
            print(ele.is_stale)

*   **Common problems and solutions**

    Browser automation is hard, specially given the dynamic nature of today's webpages. There are issues with page load, elements 
    getting refreshed in the background, lazy loading and so on. ``pybrowser`` comes with a toolkit to handle some of the most 
    common issues that can occur during browser automation.

    *   **Wait for page load**

        When you visit a page, even though Selenium waits for the page load by default, I have experienced issues with this 
        behavior. So here are couple of ways to tackle that issue.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("http://url")
                #keeps polling until page is loaded up until wait_time
                b.wait_for_page_load(wait_time=10)
                #waits until element is found up until wait_time
                b.wait_for_element(locator="id:=element", visible=True, wait_time=10)
    
    *   **Element related**

        Some of the common issues with element are element not found, not enabled, element going stale after finding etc.
        ``pybrowser's`` toolkit provides some interesting interfaces to handle such issues.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("http://url")
                #below line doesn't throw error if element is not found
                e = b.element("id:=element")
                #true if element is found
                print(e.is_found)
                #performs action only if found    
                e.if_found.click()
                #true if element was found
                print(e.is_found)
                #true if element is displayed
                print(e.is_displayed)
                #same as is_displayed
                print(e.is_visible)
                #returns id only if displayed
                print(e.if_displayed.text)
                #true if element is enabled
                print(e.is_enabled)
                e.if_enabled.move_to_element()
                #true if element has gone stale
                print(e.is_stale)
                #if you know element is going to go stale, wait for the same to happen
                e.wait_for_staleness(wait_time=10)
                #if element has gone stale, calling refresh finds element again
                e.if_stale.refresh()
                #just waits for give time
                e.wait(wait_time=10)
                #since properties of an element is cached, if you wan't to refresh cache,
                #do below (to find element again)
                e.refresh()
        
        Basically properties such as ``is_found``, ``is_displayed``, ``is_visible``, ``is_enabled``, ``is_stale`` 
        are flags available to precheck corresponding condition. And then there are properties such as
        ``if_found``, ``if_displayed``, ``if_visible``, ``if_enabled``, ``if_stale`` provide ways to conditionally
        perform actions on elements you are dealing with.
        
    
    *   **Post click**

        This issue is kind of similar to page load. When user clicks on an element (like a link or a button etc), even though
        Selenium waits for page to be ready post the action, there have been issues with that. To resolve this issue, ``pybrowser`` provides an
        interface where user can provide a hook function (should be callable) to which webdriver instance would be passed and user can
        then have specific logic to handle page/ element refresh issue after click. If hook function isn't provided there is a default wait function
        in-built which should work most of the times.

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                b.goto("http://url")
                #user_func is called as user_func(webdriver) post the click action
                e.click(hook=user_func)
                #same behavior below as well
                e.submit(hook=user_func)
                #invokes default wait function post click
                e.click()
                #if there is no easy way to handle this, just wait after click or submit
                e.wait(wait_time=10)               

**Non Browser mode**
--------------------
**pybrowser** is much more than browser automation. One of the idea behind ``pybrowser`` was to make it an interface to all things 
HTTP. So with that in mind, you can do the following with ``pybrowser``

*   **Access HTML & parse**

    You saw an example of accessing HTML object above via browser. You don't have to open a browser (such as Chrome) for that.
    Instead directly get html for the url and play around with that.

    *   **Get HTML directly**

        .. code-block:: python

            #note that even though you are using Browser(), you don't provide any
            #browser and hence no browser is opened
            with Browser() as b:
                h = b.html(url="https://the-internet.herokuapp.com/login")
                print(h)
                print(h.text)
    
    *   **Search in HTML**

        You can search in html for a specific template like below.
        More on string formatting `format-string <https://docs.python.org/3/library/string.html#format-string-syntax>`_

        .. code-block:: python

            #Look for some dynamic value
            with Browser() as b:
                h = b.html(url="http://dollarrupee.in/")
                search_text = "Current USD to INR exchange rate equals {} Rupees per 1 US Dollar"
                #note that use_text=True uses actual text content of the html.
                #If this is False (default) HTML content is used instead
                result = h.search(search_text, use_text=True)
                print(result)
                if result:
                    for r in result:
                        print(r)
            
            #You can also search for multiple occurrences of a template
            with Browser() as b:
                h = b.html(url="http://chromedriver.chromium.org/downloads")
                search_text = "ChromeDriver {} "
                result = h.search_all(search_text, use_text=True)
                for r in result:
                    for d in r:
                        print(d)
    
    *   **Find elements**

        Search for HTML elements by their attributes

        .. code-block:: python

            #Look for some dynamic value
            with Browser() as b:
                h = b.html(url="http://url/")
                e1 = h.elements.find_by_id("some_id")
                e2 = h.elements.find_by_class("some_cssclass")
                #lxml style find rel links (<a rel="tag"> Tag 1 </a>)
                e3 = h.elements.rel_links("rel")
                e4 = h.elements.find_by_css_selector("div > a")
                e5 = h.elements.find_by_xpath("//div/a")
                #returns list of tuple of link text and url
                #below returns a list of named_tuple with name and url
                e6 = h.elements.links(containing="some_text", url_only=True, images=False)  
    
    *   **Render**

        If your HTML contains javascript that needs rendering then use this. You can also evaluate your own javascript

        .. warning::  This uses `puppeteer <https://developers.google.com/web/tools/puppeteer/>`_ from Google which basically uses headless chrome and requires it's own version of chromium. So using render for the first time downloads chromium to PYPPETEER_HOME. Make sure there is right access to this folder

        .. code-block:: python

            with Browser() as bro:
                s = '''() => {
                return {
                    width: document.documentElement.clientWidth,
                    height: document.documentElement.clientHeight,
                    deviceScaleFactor: window.devicePixelRatio,
                }
                }'''
                h = bro.html(url="https://the-internet.herokuapp.com/")
                r = h.render(script=s)
                print(r)

    *   **Save**

        You can of course save the HTML

        .. code-block:: python

            with Browser(browser_name=Browser.CHROME) as b:
                h = b.goto("http://google.com").html()
                #guesses path
                save_path = h.save()
                #you can provide filename
                save_path = h.save(filename='filename.html')
                #complete path without filename
                save_path = h.save(filename='/path/to/dir')
                #complete path with filename
                save_path = h.save(filename='/path/to/dir/filename.html')

*   **Requests - Yes !**

    `Requests <http://docs.python-requests.org/en/master/>`_ has become synonym for anything HTTP 
    in python community. So how can we not use requests in ``pybrowser`` ? So we do. Two of the most common HTTP methods,
    GET and POST are supported out of the box (with asynchronous). And since ``pybrowser`` isn't restrictive, you get access to requests-session 
    object which can be used to do anything HTTP.

    .. code-block:: python

        #Look for some dynamic value
        with Browser() as b:
            #this is a blocking call
            r = b.get(url="http://url/", headers={'k':'v'})
            #text (str)  
            rt = r.content(raw=False)
            #bytes
            rb = r.content(raw=True)
            #if json
            rj = r.json
            rh = r.response_headers
            rc = r.response_code
            re = r.response_encoding
            #response object itself
            obj = r.response
            #non blocking, returns immediately
            rp = b.post(url="http://url/", body= {'b':'d'} headers={'k':'v'}, asynch=True)
            #non blocking
            if rp.is_request_done:
                #this is a blocking call on it's own
                rp = rp.result
            rpt = rp.content()
            #and so on...

**Environment variables**
-------------------------
Below are some of the environment variables that can be set via ``os.environ[name]=value``. Defaults are assumed in case one is
not provided

*   ``PYBROWSER_HOME_DIR_PATH`` : Path under which all files will be stored. Default is user home
*   ``PYBROWSER_DIR_NAME`` : pybrowser main directory name. Default is ``pybrowser``
*   ``DRIVERS_DOWNLOAD_DIR_NAME`` : directory name where webdriver files will be saved. This will be under ``PYBROWSER_DIR_NAME``. Default is browserdrivers 
*   ``HTML_DIR_NAME`` : directory name where HTML files will be saved. This will be under ``PYBROWSER_DIR_NAME``. Default is html
*   ``SCREENSHOTS_DIR_NAME`` : directory name where screenshots will be saved. This will be under ``PYBROWSER_DIR_NAME``. Default is screenshots
*   ``PYPPETEER_DIR_NAME`` : directory name where puppeteer files will be saved. This will be under ``PYBROWSER_DIR_NAME``. Default is puppeteer
*   ``PYPPETEER_HOME`` : Path where all puppeteer files would go. If this is present ``PYPPETEER_DIR_NAME`` has no significance
*   ``DEFAULT_LOGGER_PATH`` : Path under which log files will be stored. Default is under ``PYBROWSER_HOME_DIR_PATH``
*   ``DEFAULT_LOGGER_NAME`` : Name for the logger to use. Default is pybrowser
*   ``CHROME_HOME_URL`` : Home page URL for chromedriver
*   ``CHROME_DOWNLOAD_URL`` : Download URL for chromedriver. Note that is a complete url upon click should download file
*   ``CHROMEDRIVER_VERSION`` : Specific chromedriver version to use. Default is pulled from ``CHROME_HOME_URL`` (latest version)
*   ``IE_HOME_URL`` : Home page URL for IEdriver
*   ``IE_DOWNLOAD_URL`` : Download URL for IEdriver. Note that is a complete url upon click should download file
*   ``IEDRIVER_VERSION`` : Specific IEdriver version to use. Default currently is 3.14
*   ``FIREFOX_HOME_URL`` : Home page URL for IEdriver
*   ``FIREFOX_DOWNLOAD_URL`` : Download URL for IEdriver. Note that is a complete url upon click should download file
*   ``FIREFOXDRIVER_VERSION`` : Specific IEdriver version to use. Default currently is 3.14

**Logging**
-----------
**pybrowser** comes with default logger (``pybrowser``). Same can be used in your application as well.
You can of course use above environment variables related to logger to set your own name and path. You can give any name
during execution as well (see below). Example code below.

.. code-block:: python

    from pybrowser import log_adapter
    #not providing logger_name uses default
    log = log_adapter.get_logger(logger_name="some_name")
    log.info("logging")
    #current name will be remembered for the run and you can use
    #log_adapter.get_logger() afterwards

**Contributing to pybrowser**
-----------------------------
**pybrowser** is an open source project under MIT license. That means you are allowed to use it the way you wish.
If you are a developer and want to contribute, please feel free to send pull requests. You can also contribute with testing,
feature suggestion and/or addition, defect fixes, documentation etc
     
Indices and tables
******************

* :ref:`search`
