# -*- coding: utf-8 -*-
from openerp.addons.currency_rate_update.\
    services.currency_getter import Currency_getter_factory, UnknowClassError


class CurrencyGetterFactoryTHB(Currency_getter_factory):
    """Factory pattern class that will return
    a currency getter class base on the name passed
    to the register method
    """

    def register(self, class_name):
        """ for class_name = 'THB_getter' """
        print '------------------th_register -- %s' % class_name
        if class_name != 'THB_getter':
            return Currency_getter_factory.register(self, class_name)
        else:
            exec "from .update_service_%s import %s" % \
                 (class_name.replace('_getter', ''), class_name)
            class_def = eval(class_name)
            print class_def
            return class_def()
