import os
from lxml import html
from lxml.html.clean import Cleaner
from .common_utils import (is_valid_url, get_unique_filename_from_url, get_user_home_dir, 
                           make_dir, dir_filename)
from .external.parse import search as parse_search
from .external.parse import findall
from .external.htmlrenderer import render_html
from .constants import CONSTANTS

LINESEP = os.linesep

class HTML(object):

    def __init__(self, content=None, url=None, encoding="utf-8", print_style=False, print_js=True, 
                 remove_tags=None):
        self._set_content(content, encoding)
        self.encoding = encoding
        self.url = url
        self.lxmltree = html.fromstring(self.content)
        self.cleaner = self._get_cleaner(print_style, print_js, remove_tags)
    
    def __str__(self):
        return html.tostring(self.cleaner.clean_html(self.lxmltree), pretty_print=True, encoding='unicode')
    
    def _set_content(self, content, encoding):
        self.content = None
        if isinstance(content, bytes):
            self.content = content.decode(encoding=encoding, errors="ignore")
        else:
            self.content = str(content).encode(encoding=encoding, errors='ignore').decode()
    
    def _get_cleaner(self, print_style, print_js, remove_tags):
        c = Cleaner()
        c.scripts = not print_js
        c.javascript = not print_js
        c.style = not print_style
        c.remove_tags = remove_tags
        c.page_structure = False
        return c
    
    @property
    def text(self):
        if self.lxmltree is None:
            return
        s = self.lxmltree.text_content()
        #TODO: might need a performance fix in future
        if isinstance(s, str):
            s = LINESEP.join([t.strip() for t in s.split(LINESEP) if t and t.strip()])
        return s 
    
    @property
    def elements(self):
        return Elements(self.lxmltree, self.encoding)
    
    def search(self, template, use_text=False):
        """Search the :class:`Element <Element>` for the given Parse template.

        :param template: The Parse template to use.
        """
        c = self.text if use_text else self.content
        return parse_search(template, c)

    def search_all(self, template, use_text=False):
        """Search the :class:`Element <Element>` (multiple times) for the given parse
        template.

        :param template: The Parse template to use.
        """
        c = self.text if use_text else self.content
        return [r for r in findall(template, c)]
    
    def save(self, filename=None):
        final_path = self._get_filename_from_url(filename)
        with open(final_path, "w", encoding=self.encoding) as f:
            f.write(self.content)
    
    def _get_filename_from_url(self, filename=None):
        if filename is None:
            f = get_unique_filename_from_url(self.url, ext="html")
            d = os.path.join(get_user_home_dir(), CONSTANTS.DIR_NAME, CONSTANTS.HTML_DIR)
        else:        
            d, f = dir_filename(filename, default_ext="html")
            if not d:
                d = os.path.join(get_user_home_dir(), CONSTANTS.DIR_NAME, CONSTANTS.HTML_DIR)
            if not f:
                f = get_unique_filename_from_url(self.driver.current_url, ext="html")
        make_dir(d)
        #final path 
        return os.path.join(d, f)
    
    def render(self, script=None, text=False):
        result, content = render_html(url=self.url, html=self.content, get_text=text, script=script, reload=False)
        if content:
            self.content = content
        #script execution results
        return result
    
class Elements(object):

    def __init__(self, lxmltree, encoding):
        self.lxmltree = lxmltree
        self.encoding = encoding

    def find_by_id(self, id_):
        if not (id_ and self.lxmltree):
            return
        return self.lxmltree.get_element_by_id(id_)
    
    def find_by_class(self, clazz):
        if not (clazz and self.lxmltree):
            return
        return self.lxmltree.find_class(clazz)

    def rel_links(self, rel):
        #Find any links like ``<a rel="{rel}">...</a>``; returns a list of elements.
        if not (rel and self.lxmltree):
            return
        return self.lxmltree.find_rel_links(rel)
    
    def find_by_css_selector(self, selector):
        if not (selector and self.lxmltree):
            return
        return self.lxmltree.cssselect(selector)
       
    def find_by_xpath(self, selector):
        if not (selector and self.lxmltree):
            return
        return self.lxmltree.xpath(selector)
    
    def links(self, containing=None, url_only=True):
        if self.lxmltree is None:
            return
        links_ = []
        for element, attribute, link, pos in self.lxmltree.iterlinks():
            if containing and containing not in element.text_content():
                continue
            link_key = self._get_element_text_content(element.text_content()) or attribute
            if url_only:
                if is_valid_url(link):
                    links_.append((link_key, link))
            else:
                links_.append((link_key, link))
        return links_
    
    def _get_element_text_content(self, text, limit=100):
        if isinstance(text, bytes):
            text = text.decode(encoding=self.encoding, errors="ignore")
        else:
            text = str(text).encode(encoding=self.encoding, errors='ignore').decode()
        text = text.strip() if text else ""
        return text[:limit]
