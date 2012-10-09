# (c) 2009, J Kenneth King
#
# Licensed under LGPLv3
#
# See http://www.gnu.org/licenses/lgpl-3.0.txt for license details
#
# This module provides the ESelectPlus interface to the Moneris
# eSelectPlus API.  It is a wrapper around the code I ported from
# Perl.  It should reduce the amount of bloat in your application's
# code.

import api


class ESelectPlus(object):

    def __init__(self, store_id, api_token, host, port, path, timeout=3600):
        self._server = api.Server(store_id,
                                  api_token,
                                  protocol='https',
                                  host=host,
                                  port=port,
                                  path=path,
                                  timeout=timeout)

    def purchase(self, order_id, cust_id, amount, cc_number,
                 exp_date, crypt_type='7', street_num=None,
                 street_name=None, zip_code=None):
        """
        If you store the customer's CC on your servers, this is the
        method you want to call to initiate a purchase.  The kwarg
        parameters are optional (but all are required if you use them)
        and are used to add additional verification metrics.

        >>> processor = ESelectPlus('moneris', 'hurgle', 'esqa.moneris.com',
        ...                         '443', '/gateway2/servlet/MpgRequest')
        >>> res = processor.purchase('1', '42', '0.99', '4242424242424242',
        ...                          '1010', '7')
        """
        txn = api.Transaction(dict(
                type='purchase',
                cust_id=cust_id,
                amount=amount,
                pan=cc_number,
                expdate=exp_date,
                crypt_type=crypt_type))

        if street_num and street_name and zip_code:
            txn.add_avs_info(street_num, street_name, zip_code)

        res = self._server.do_request(txn)
