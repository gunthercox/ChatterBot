"""
Add GitHub repository details to the Sphinx context.
"""

GITHUB_USER = 'gunthercox'
GITHUB_REPO = 'ChatterBot'

def setup_github_func(app, pagename, templatename, context, doctree):
    """
    Return the url to the specified page on GitHub.
    """

    github_version = 'master'
    docs_path = 'docs'

    def my_func():
        return f'https://github.com/{GITHUB_USER}/{GITHUB_REPO}/blob/{github_version}/{docs_path}/{pagename}.rst'

    # Add it to the page's context
    context['github_page_link'] = my_func


# Extension setup function
def setup(app):
    app.connect('html-page-context', setup_github_func)
