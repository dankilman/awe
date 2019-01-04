project = 'awe'
copyright = '2019, Dan Kilman'
author = 'Dan Kilman'
extensions = ['sphinx.ext.viewcode', 'sphinx.ext.autodoc']
master_doc = 'index'
html_theme = 'alabaster'
html_theme_options = {
    'description': 'Dynamic web based reports/dashboards in Python',
    'github_user': 'dankilman',
    'github_repo': project,
    'fixed_sidebar': True,
    'page_width': '1000px',
}
autodoc_member_order = 'bysource'
autoclass_content = 'both'
