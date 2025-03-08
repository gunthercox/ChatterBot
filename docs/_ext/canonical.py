"""
Add GitHub repository details to the Sphinx context.
"""

def setup_canonical_func(app, pagename, templatename, context, doctree):
    """
    Return the url to the specified page on GitHub.

    (Sphinx 7.4 generates a canonical link with a .html extension even
    when run in dirhtml mode)
    """

    conf = app.config

    def canonical_func():
        # Special case for the root index page
        if pagename == 'index':
            return conf.html_baseurl

        dir_name = pagename.replace('/index', '/')
        return f'{conf.html_baseurl}{dir_name}'

    # Add it to the page's context
    context['canonical_url'] = canonical_func


# Extension setup function
def setup(app):
    app.connect('html-page-context', setup_canonical_func)
