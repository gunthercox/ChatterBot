import os
import sys
import configparser
from datetime import datetime
import sphinx_rtd_theme


config = configparser.ConfigParser()

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
config_file_path = os.path.join(parent_directory, 'setup.cfg')

config.read(config_file_path)

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and used to generate the documentation.
sys.path.insert(0, parent_directory)


# Sphinx extension modules
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']

# The encoding of source files
# source_encoding = 'utf-8-sig'

# The master toctree document
master_doc = 'index'

# General information about the project
project = 'ChatterBot'
author = config['chatterbot']['author']
copyright = '{}, {}'.format(
    datetime.now().year,
    author
)

# The full version, including alpha/beta/rc tags
release = config['chatterbot']['version']

# The short X.Y version
version = config['chatterbot']['version'].rsplit('.', 1)[0]

language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# If true, '()' will be appended to :func: etc. cross-reference text
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::)
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# Theme options are theme-specific and customize the look and feel of a theme
# further. For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'logo_only': True
}

html_show_sourcelink = False

# A shorter title for the navigation bar. Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '../graphics/banner.png'

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
# html_last_updated_fmt = None

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# Split the index into individual pages for each letter.
html_split_index = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr', 'zh'
html_search_language = 'en'

# Output file base name for HTML help builder
htmlhelp_basename = 'ChatterBotdoc'

# Read the docs theme modifications

html_context = {
    'extra_css_files': [
        '_static/style.css'
    ]
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class])
latex_documents = [
    (master_doc, 'ChatterBot.tex', u'ChatterBot Documentation',
     u'Gunther Cox', 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section)
man_pages = [
    (master_doc, 'chatterbot', u'ChatterBot Documentation',
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'ChatterBot', u'ChatterBot Documentation',
     author, 'ChatterBot', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# A list of files that should not be packed into the epub file
epub_exclude_files = ['search.html']

# Configuration for intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None)
}
