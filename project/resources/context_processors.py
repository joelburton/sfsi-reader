"""
Context processors related to resources.

These are things which are added to the request object.
"""

# Site-wide navigation
#
# (Name, Absolute URL, glyphicon name to use

NAV = [
    ('Days', '/days/', 'calendar'),
    ('Topics', '/topics/', 'list-alt'),
    ('Key Resources', '/key-resources/', 'star'),
    ('Required', '/required/', 'exclamation-sign'),
]


def site_nav(request):
    """Add site navigation to request.

    Adds a CSS class of active if we're within that part of the site.
    """

    in_ = request.path.startswith

    return {
        'site_nav':
            [
                {
                    'title': title,
                    'path': path,
                    'glyph': glyph,
                    'class': 'active' if in_(path) else ''
                }
                for title, path, glyph in NAV
            ]
    }