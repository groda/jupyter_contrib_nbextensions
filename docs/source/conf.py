#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# jupyter_contrib_nbextensions sphinx documentation build configuration file.
# This file gets execfile()d with the current directory set to its containing
# dir.

import datetime
import glob
import logging
import os

from jupyter_contrib_core.testing_utils import get_logger
from recommonmark.transform import AutoStructify
from recommonmark.parser import CommonMarkParser

log = get_logger(name=os.path.basename(__file__), log_level=logging.INFO)

# Set on_rtd to whether we are building on readthedocs. We get this test from
# docs.readthedocs.io
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
log.info('on_rtd = {}'.format(on_rtd))

# mappings to other sphinx docs
intersphinx_mapping = {
    'ipython': ('http://ipython.org/ipython-doc/dev/', None),
    'nbconvert': ('http://nbconvert.readthedocs.io/en/latest/', None),
    'nbformat': ('http://nbformat.readthedocs.io/en/latest/', None),
    'notebook': ('http://jupyter-notebook.readthedocs.io/en/latest/', None),
    'jupyter': ('http://jupyter.readthedocs.io/en/latest/', None),
    'traitlets': ('http://traitlets.readthedocs.io/en/latest/', None),
}

# General information about the project.
project = 'jupyter_contrib_nbextensions'
copyright = '2015-{}, Jupyter Contrib Team'.format(datetime.date.today().year)
author = 'Jupyter Contrib Team'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.2.6'
# The full version, including alpha/beta/rc tags.
release = '0.2.6'

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of strings
source_suffix = ['.rst', '.md']
source_parsers = {'.md': CommonMarkParser}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    '**/.ipynb_checkpoints',
    # the history file isn't linked to by either of the main exercise readmes
    'nbextensions/exercise/history.md',
    # slidemode2 has no yaml, so this won't be linked to in autogenerated toc
    'nbextensions/slidemode/slidemode2/README.md',
    # latex_envs includes its readme twice, but we only use one copy
    'nbextensions/latex_envs/doc/README.md',
]

# The master toctree document.
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'IPython.sphinxext.ipython_console_highlighting',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Set standard backtick role
default_role = 'code'

suppress_warnings = ['image.nonlocal_uri']

# regex patterns for the beginning of links not to check
linkcheck_ignore = [
    r'https?://(localhost|127\.0\.0\.1):\d+/',  # local links
]

# -- Options for HTML output --------------------------------------------------

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# otherwise, readthedocs.org uses their default theme, so no need to specify it

# Output file base name for HTML help builder.
htmlhelp_basename = project + '_doc'

# -- Options for LaTeX output -------------------------------------------------
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, project + '_doc.tex',
     'Jupyter-contrib Notebook Extensions Documentation', author, 'manual'),
]

# -- Options for man-page output ----------------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, project,
     'Jupyter-contrib Notebook Extensions Documentation', [author], 1)
]

# -- Options for Texinfo output -----------------------------------------------
# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, project + '_doc',
     'Jupyter-contrib Notebook Extensions Documentation', author,
     'nbextensions', 'Contributed Jupyter Notebook Extensions.',
     'Miscellaneous'),
]

# -- Run our auto-generation scripts ------------------------------------------
for autogen_path in glob.glob(os.path.join('autogen_scripts', '*.py')):
    autogen_path = os.path.realpath(autogen_path)
    log.info('> running autogen script {}'.format(
        os.path.relpath(autogen_path, os.path.dirname(__file__))))
    with open(autogen_path) as f:
        _code = compile(f.read(), autogen_path, 'exec')
        exec(_code, {'__file__': autogen_path})


def setup(app):
    if not on_rtd:
        from readthedocs_ext.readthedocs import ReadtheDocsBuilder
        app.add_builder(ReadtheDocsBuilder)

    def resolve_url(url):
        """Return path to code file given relative url."""
        github_root = ('https://github.com/ipython-contrib/' +
                       'jupyter_contrib_nbextensions/blob/master/' +
                       'src/jupyter_contrib_nbextensions/')
        return github_root + url.replace(os.path.sep, '/')

    app.add_config_value('recommonmark_config', dict(
        enable_auto_toc_tree=True,
        auto_toc_tree_section='Contents',
        enable_auto_doc_ref=True,
        enable_math=True,
        enable_inline_math=True,
        url_resolver=resolve_url,
        enable_eval_rst=False,
    ), True)
    app.add_transform(AutoStructify)
