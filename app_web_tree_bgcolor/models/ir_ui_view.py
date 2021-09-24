# -*- coding: utf-8 -*-
import ast
import logging
import os

from lxml import etree

from odoo import api, fields, models, tools
from odoo.tools import view_validation
from odoo.tools.view_validation import _relaxng_cache

_logger = logging.getLogger(__name__)
# attributes in views that may contain references to field names
ATTRS_WITH_FIELD_NAMES_2 = {
    'bg-danger',
    'bg-info',
    'bg-muted',
    'bg-primary',
    'bg-success',
    'bg-warning',
}


def relaxng_bg(view_type):
    """ Return a validator for the given view type, or None. """
    ADDONS_PATH = tools.config['addons_path']
    if view_type not in _relaxng_cache:
        # 先判断 search 和 tree
        if (view_type == 'search'):
            folder = 'app_web_superbar'
        elif (view_type == 'tree'):
            folder = 'app_web_tree_bgcolor'
        else:
            folder = 'base'
        _file = '%s/rng/%s_view.rng' % (folder, view_type)

        try:
            with tools.file_open(_file) as frng:
                try:
                    relaxng_doc = etree.parse(frng)
                    _relaxng_cache[view_type] = etree.RelaxNG(relaxng_doc)
                except Exception:
                    _logger.exception('%s Failed to load RelaxNG XML schema for views validation' % _file)
                    _relaxng_cache[view_type] = None
        except Exception:
            # 出错时到base找
            _file = 'base/rng/%s_view.rng' % (view_type)
            with tools.file_open(os.path.join(_file)) as frng:
                try:
                    relaxng_doc = etree.parse(frng)
                    _relaxng_cache[view_type] = etree.RelaxNG(relaxng_doc)
                except Exception:
                    _logger.exception('%s Failed to load RelaxNG XML schema for views validation' % _file)
                    _relaxng_cache[view_type] = None
    return _relaxng_cache[view_type]

class View(models.Model):
    _inherit = 'ir.ui.view'

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        view_validation.relaxng = relaxng_bg

    def get_attrs_field_names(self, arch, model, editable):
        symbols = self.get_attrs_symbols() | {None}
        result = []

        def get_name(node):
            """ return the name from an AST node, or None """
            if isinstance(node, ast.Name):
                return node.id

        def process_expr(expr, get, key, val):
            """ parse `expr` and collect triples """
            for node in ast.walk(ast.parse(expr.strip(), mode='eval')):
                name = get(node)
                if name not in symbols:
                    result.append((name, key, val))

        def add_bg(node, model, editable, get=get_name):
            for key, val in node.items():
                if not val:
                    continue
                if key in ATTRS_WITH_FIELD_NAMES_2:
                    process_expr(val, get, key, val)

        res = super(View, self).get_attrs_field_names(arch, model, editable)
        add_bg(arch, model, editable)
        res += result
        return res


