project = 'awe'
copyright = '2019, Dan Kilman'
author = 'Dan Kilman'
extensions = ['sphinx.ext.viewcode', 'sphinx.ext.autodoc']
master_doc = 'index'
html_static_path = ['_static']
html_theme = 'alabaster'
html_theme_options = {
    'description': 'Dynamic web based reports/dashboards in Python',
    'github_user': 'dankilman',
    'github_repo': project,
    'github_type': 'star',
    'fixed_sidebar': True,
    'page_width': '1200px'
}
autodoc_member_order = 'bysource'
autoclass_content = 'both'
