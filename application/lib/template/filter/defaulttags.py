#!/usr/bin/env python
#coding: utf-8
#auth:   www
#create: 12-11-10 下午5:08
#desc: 
from __future__ import division

from django.template.base import Node, Library,TemplateSyntaxError, VariableDoesNotExist

register = Library()


class WidthRatioNode(Node):
    def __init__(self, val_expr, max_expr, max_width):
        self.val_expr = val_expr
        self.max_expr = max_expr
        self.max_width = max_width

    def render(self, context):
        try:
            value = self.val_expr.resolve(context)
            max_value = self.max_expr.resolve(context)
            max_width = int(self.max_width.resolve(context))
        except VariableDoesNotExist:
            return ''
        except ValueError:
            raise TemplateSyntaxError("widthratio final argument must be an number")
        try:
            value = float(value)
            max_value = float(max_value)
            ratio = (value / max_value) * max_width
        except ZeroDivisionError:
            return '0'
        except ValueError:
            return ''
        return '%.2f' % ratio

@register.tag
def widthratio(parser, token):
    """
    For creating bar charts and such, this tag calculates the ratio of a given
    value to a maximum value, and then applies that ratio to a constant.

    For example::

        <img src='bar.gif' height='10' width='{% widthratio this_value max_value 100 %}' />

    Above, if ``this_value`` is 175 and ``max_value`` is 200, the image in
    the above example will be 88 pixels wide (because 175/200 = .875;
    .875 * 100 = 87.5 which is rounded up to 88).
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError("widthratio takes three arguments")
    tag, this_value_expr, max_value_expr, max_width = bits

    return WidthRatioNode(parser.compile_filter(this_value_expr),
        parser.compile_filter(max_value_expr),
        parser.compile_filter(max_width))
