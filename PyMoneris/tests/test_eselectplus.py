import unittest

from pymoneris.eselectplus.api import Server, Transaction


# TODO: Move XML expected_output into stub files

class TestESelectPlusAPI(unittest.TestCase):
    """
    This module is as direct a port of the Perl API v.2.0.4 as is
    possible.  As such we test against the exact XML ouput by that
    API.
    """

    def setUp(self):
        self.svr = Server('moneris', 'hurgle')

    def test_add_cc(self):
        expected_out = ('<?xml version="1.0"?><request><store_id>moneris'
                        '</store_id><api_token>hurgle</api_token><res_add_cc>'
                        '<cust_id>mj</cust_id><phone>1-800-555-5555</phone>'
                        '<email>hello@world.com</email><note>I have no note'
                        '</note><pan>4242424242424242</pan><expdate>0901'
                        '</expdate><crypt_type>1</crypt_type><avs_info>'
                        '<avs_street_number>123</avs_street_number>'
                        '<avs_street_name>East Street</avs_street_name>'
                        '<avs_zipcode>M1M2M2</avs_zipcode></avs_info>'
                        '</res_add_cc></request>')
        txn = Transaction(type='res_add_cc',
                          cust_id='mj',
                          phone='1-800-555-5555',
                          email='hello@world.com',
                          note='I have no note',
                          pan='4242424242424242',
                          expdate='0901',
                          crypt_type='1')
        txn.add_avs_info('123', 'East Street', 'M1M2M2')
        # we call the internal _to_xml() which is called by the
        # do_request method in order to bypass actually performing the
        # request, parsing response xml, etc, etc.  We'll be doing
        # this through out the rest of this test case.
        test_out = self.svr._to_xml(txn)
        assert test_out == expected_out

    def test_delete(self):
        expected_out = ('<?xml version="1.0"?><request><store_id>moneris'
                        '</store_id><api_token>hurgle</api_token>'
                        '<res_delete><data_key>2OP363681nd1xxV7Kka3I986w'
                        '</data_key></res_delete></request>')
        txn = Transaction(type='res_delete',
                          data_key='2OP363681nd1xxV7Kka3I986w')
        test_out = self.svr._to_xml(txn)
        assert test_out == expected_out

    def test_get_expiring(self):
        expected_out = ('<?xml version="1.0"?><request><store_id>moneris'
                        '</store_id><api_token>hurgle</api_token>'
                        '<res_get_expiring></res_get_expiring></request>')
        txn = Transaction(type='res_get_expiring')
        test_out = self.svr._to_xml(txn)
        assert test_out == expected_out

    def test_ind_refund_cc(self):
        expected_out = ('<?xml version="1.0"?><request><store_id>moneris'
                        '</store_id><api_token>hurgle</api_token>'
                        '<res_ind_refund_cc><data_key>C181e5921rj5v1iaKS'
                        'Mf83q86</data_key><order_id>res-ind-refund-1289'
                        '066727</order_id><cust_id>mj</cust_id><amount>'
                        '1.00</amount><crypt_type>7</crypt_type>'
                        '</res_ind_refund_cc></request>')
        txn = Transaction(type='res_ind_refund_cc',
                          data_key='C181e5921rj5v1iaKSMf83q86',
                          order_id='res-ind-refund-1289066727',
                          cust_id='mj',
                          amount='1.00',
                          crypt_type='7')
        test_out = self.svr._to_xml(txn)
        assert test_out == expected_out

    def test_is_corporatecard(self):
        expected_out = ('<?xml version="1.0"?><request><store_id>moneris'
                        '</store_id><api_token>hurgle</api_token>'
                        '<res_iscorporatecard><data_key>9A143sx23Y2Sb426'
                        'J45GXYYM8</data_key></res_iscorporatecard>'
                        '</request>')
        txn = Transaction(type='res_iscorporatecard',
                          data_key='9A143sx23Y2Sb426J45GXYYM8')
        test_out = self.svr._to_xml(txn)
        assert test_out == expected_out

    def test_lookup_full(self):
        expected_out = ('<?xml version="1.0"?><request><store_id>moneris'
                        '</store_id><api_token>hurgle</api_token>'
                        '<res_lookup_full><data_key>C181e5921rj5v1iaKSMf'
                        '83q86</data_key></res_lookup_full></request>')
        txn = Transaction(type='res_lookup_full',
                          data_key='C181e5921rj5v1iaKSMf83q86')
        test_out = self.svr._to_xml(txn)
        assert test_out == expected_out

    def test_lookup_masked(self):
        expected_out = ('<?xml version="1.0"?><request><store_id>moneris'
                        '</store_id><api_token>hurgle</api_token>'
                        '<res_lookup_masked><data_key>C181e5921rj5v1iaKS'
                        'Mf83q86</data_key></res_lookup_masked></request>')
        txn = Transaction(type='res_lookup_masked',
                          data_key='C181e5921rj5v1iaKSMf83q86')
        test_out = self.svr._to_xml(txn)
        assert test_out == expected_out

    def test_preauth_custinfo(self):
        expected_out = ('<?xml version="1.0"?><request><store_id>moneris</st'
                        'ore_id><api_token>hurgle</api_token><res_preauth_cc'
                        '><data_key>C181e5921rj5v1iaKSMf83q86</data_key><ord'
                        'er_id>res-preauth-1289067953</order_id><cust_id>mj<'
                        '/cust_id><amount>1.00</amount><crypt_type>7</crypt_'
                        'type><cust_info><email>Joe@widgets.com</email><inst'
                        'ructions>Make it fast</instructions><billing><first'
                        '_name>Joe</first_name><last_name>Thompson</last_nam'
                        'e><company_name>Widget Company Inc.</company_name><'
                        'address>111 Bolts Ave.</address><city>Toronto</city'
                        '><province>Ontario</province><postal_code>M8T 1T8</'
                        'postal_code><country>Canada</country><phone_number>'
                        '416-555-5555</phone_number><fax>416-555-5555</fax><'
                        'tax1>123.45</tax1><tax2>12.34</tax2><tax3>15.45</ta'
                        'x3><shipping_cost>456.23</shipping_cost></billing><'
                        'shipping><first_name>Joe</first_name><last_name>Tho'
                        'mpson</last_name><company_name>Widget Company Inc.<'
                        '/company_name><address>111 Bolts Ave.</address><cit'
                        'y>Toronto</city><province>Ontario</province><postal'
                        '_code>M8T 1T8</postal_code><country>Canada</country'
                        '><phone_number>416-555-5555</phone_number><fax>416-'
                        '555-5555</fax><tax1>123.45</tax1><tax2>12.34</tax2>'
                        '<tax3>15.45</tax3><shipping_cost>456.23</shipping_c'
                        'ost></shipping><item><name>item 1 name</name><quant'
                        'ity>53</quantity><product_code>item 1 product code<'
                        '/product_code><extended_amount>1.00</extended_amoun'
                        't></item><item><name>item 2 name</name><quantity>53'
                        '</quantity><product_code>item 2 product code</produ'
                        'ct_code><extended_amount>1.00</extended_amount></it'
                        'em></cust_info></res_preauth_cc></request>')
        txn = Transaction(type='res_preauth_cc',
                          data_key='C181e5921rj5v1iaKSMf83q86',
                          order_id='res-preauth-1289067953',
                          cust_id='mj',
                          amount='1.00',
                          crypt_type='7')
        billing = dict(first_name='Joe',
                       last_name='Thompson',
                       company_name='Widget Company Inc.',
                       address='111 Bolts Ave.',
                       city='Toronto',
                       province='Ontario',
                       postal_code='M8T 1T8',
                       country='Canada',
                       phone_number='416-555-5555',
                       fax='416-555-5555',
                       tax1='123.45',
                       tax2='12.34',
                       tax3='15.45',
                       shipping_cost='456.23')
        shipping = dict(first_name='Joe',
                        last_name='Thompson',
                        company_name='Widget Company Inc.',
                        address='111 Bolts Ave.',
                        city='Toronto',
                        province='Ontario',
                        postal_code='M8T 1T8',
                        country='Canada',
                        phone_number='416-555-5555',
                        fax='416-555-5555',
                        tax1='123.45',
                        tax2='12.34',
                        tax3='15.45',
                        shipping_cost='456.23')
        items = [dict(name='item 1 name', 
                      quantity='53', 
                      product_code='item 1 product code',
                      extended_amount='1.00'),
                 dict(name='item 2 name', 
                      quantity='53', 
                      product_code='item 2 product code',
                      extended_amount='1.00')]
        txn.add_cust_info(email='Joe@widgets.com',
                          instructions='Make it fast',
                          shipping=shipping,
                          billing=billing,
                          item=items)
        test_out = self.svr._to_xml(txn)
        assert test_out == expected_out
