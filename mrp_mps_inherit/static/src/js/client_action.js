odoo.define('mrp_mps_inherit.ClientAction', function (require) {
'use strict';

    var ClientAction = require('mrp_mps.ClientAction');

    ClientAction.include({
        events: _.extend({}, ClientAction.prototype.events, {
            'change .o_mrp_mps_input_agricultural_production_qty': '_onChangeAgricultural',
            'focus .o_mrp_mps_input_agricultural_production_qty': '_onFocusAgricultural',
            'change .o_mrp_mps_input_purchases_qty': '_onChangePurchase',
            'focus .o_mrp_mps_input_purchases_qty': '_onFocusPurchase',
        }),

        _saveAgricultural: function (productionScheduleId, dateIndex, agriculturalQty) {
            var self = this;
            this.mutex.exec(function () {
                return self._rpc({
                    model: 'mrp.production.schedule',
                    method: 'set_agricultural_qty',
                    args: [productionScheduleId, dateIndex, agriculturalQty],
                }).then(function () {
                    return self._renderProductionSchedule(productionScheduleId).then(function () {
                        return self._focusNextInput(productionScheduleId, dateIndex, 'demand_forecast');
                    });
                });
            });
        },

        _onChangeAgricultural: function (ev) {
            ev.stopPropagation();
            var $target = $(ev.target);
            var dateIndex = $target.data('date_index');
            var productionScheduleId = $target.closest('.o_mps_content').data('id');
            var agriculturalQty = parseFloat($target.val());
            if (isNaN(agriculturalQty)){
                this._backToState(productionScheduleId);
            } else {
                this._saveAgricultural(productionScheduleId, dateIndex, agriculturalQty);
            }
        },

        _onFocusAgricultural: function (ev) {
            ev.preventDefault();
            $(ev.target).select();
        },

        _savePurchase: function (productionScheduleId, dateIndex, purchaseQty) {
            debugger;
            var self = this;
            this.mutex.exec(function () {
                return self._rpc({
                    model: 'mrp.production.schedule',
                    method: 'set_purchase_qty',
                    args: [productionScheduleId, dateIndex, purchaseQty],
                }).then(function () {
                    return self._renderProductionSchedule(productionScheduleId).then(function () {
                        return self._focusNextInput(productionScheduleId, dateIndex, 'demand_forecast');
                    });
                });
            });
        },

        _onChangePurchase: function (ev) {
            ev.stopPropagation();
            var $target = $(ev.target);
            var dateIndex = $target.data('date_index');
            var productionScheduleId = $target.closest('.o_mps_content').data('id');
            var purchaseQty = parseFloat($target.val());
            if (isNaN(purchaseQty)){
                this._backToState(productionScheduleId);
            } else {
                this._savePurchase(productionScheduleId, dateIndex, purchaseQty);
            }
        },

        _onFocusPurchase: function (ev) {
            debugger;
            ev.preventDefault();
            $(ev.target).select();
        },
    });
});