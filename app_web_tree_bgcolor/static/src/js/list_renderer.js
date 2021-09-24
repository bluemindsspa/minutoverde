odoo.define('app_web_tree_bgcolor.ListRenderer', function (require) {
"use strict";

var core = require('web.core');
var ListRenderer = require('web.ListRenderer');


ListRenderer.include({
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        var DECORATIONS2 = [
            'decoration-bf',
            'decoration-it',
            'decoration-danger',
            'decoration-info',
            'decoration-muted',
            'decoration-primary',
            'decoration-success',
            'decoration-warning',
            'bg-danger',
            'bg-info',
            'bg-muted',
            'bg-primary',
            'bg-success',
            'bg-warning'
        ];
        this.rowDecorations = _.chain(this.arch.attrs)
            .pick(function (value, key) {
                return DECORATIONS2.indexOf(key) >= 0;
            }).mapObject(function (value) {
                return py.parse(py.tokenize(value));
            }).value();
    },
});
});

