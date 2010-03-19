# (c) 2009, J Kenneth King
#
# Licensed under LGPLv3
#
# See http://www.gnu.org/licenses/lgpl-3.0.txt for license details

import urllib, urllib2

from helpers import xml_to_dict

__version__ = 'MPG Version 2.02 (python)'
__all__ = ['Transaction', 'Server']

# Mpg Classes, a near direct translation from the Moneris-supplied
# Perl API interface.  AFAIK they are like optional attributes to be
# added to a request.  These classes render the xml with the
# appropriate fields in specific order for each optional attribute.

class MpgRecur(object):

    _tags = ['recur_unit', 'start_now', 'start_date',
             'num_recurs', 'period', 'recur_amount']

    def __init__(self, **params):
        self.params = params

    def _to_xml(self):
        xml_string = ''

        for tag in self._tags:
            try:
                xml_string += '<%s>%s</%s>' % (tag,
                                               self.params[tag],
                                               tag)
            except KeyError, e:
                raise AssertionError, "Missing '%s' recur field"\
                    % (tag,)

        return '<recur>%s</recur>' % (xml_string,)


class MpgCustInfo(object):

    # Beware this messy class.  Look at the official Moneris Perl API.

    _level3template = ['email', 'instructions', 'billing', 'shipping', 'item']
    _level3template_details = dict(
        email='0',
        instructions='0',
        billing=['first_name', 'last_name', 'company_name', 'address',
                 'city', 'province', 'postal_code', 'country', 'phone_number',
                 'fax','tax1', 'tax2','tax3', 'shipping_cost'],
        shipping=['first_name', 'last_name', 'company_name', 'address',
                  'city', 'province', 'postal_code', 'country',
                  'phone_number', 'fax','tax1', 'tax2', 'tax3',
                  'shipping_cost'],
        item=['name', 'quantity', 'product_code', 'extended_amount'])

    def __init__(self, email, instructions, shipping, billing, item):
        self.email = email
        self.instructions = instructions
        self.shipping = shipping
        self.billing = billing
        self.item = item

    def _to_xml(self):
        xml_string = begin_tag = end_tag = pcdata = ''

        for element in self._level3template:
            if element in ['email', 'instructions']:
                begin_tag = '<%s>' % element
                end_tag = '</%s>' % element
                try:
                    pcdata = getattr(self, element)
                except AttributeError, e:
                    raise AssertionError, "Missing cust_info field: %s"\
                        % (element,)
                xml_string += begin_tag + pcdata + end_tag
            else:
                try:
                    t_data = getattr(self, element)
                except AttributeError, e:
                    raise AssertionError, "Missing cust_info field: %s"\
                        % (element,)

                begin_tag = '<%s>' % element
                end_tag = '</%s>' % element
                inner_xml = ''

                for tag in self._level3template_details:
                    try:
                        inner_xml += '<%s>%s</%s>' % (tag,
                                                      t_data[tag],
                                                      tag)
                    except KeyError, e:
                        raise AssertionError, "Missing field %s for attr %s"\
                            % (tag, element)
                xml_string += begin_tag + inner_xml + end_tag

        return '<cust_info>%s</cust_info>' % (xml_string,)


class MpgAvsInfo(object):

    _tags = ['avs_street_number', 'avs_street_name', 'avs_zipcode']

    def __init__(self, **params):
        self.params = params

    def _to_xml(self):
        xml_string = ''

        for tag in self._tags:
            try:
                xml_string += '<%s>%s</%s>' % (tag,
                                               self.params[tag],
                                               tag)
            except KeyError, e:
                raise AssertionError, "Missing '%s' avs_info field"\
                    % (tag,)

        return '<avs_info>%s</avs_info>' % (xml_string,)


class MpgCvdInfo(object):

    _tags = ['cvd_indicator', 'cvd_value']

    def __init__(self, **params):
        self.params = params

    def _to_xml(self):
        xml_string = ''

        for tag in self._tags:
            try:
                xml_string += '<%s>%s</%s>' % (tag,
                                               self.params[tag],
                                               tag)
            except KeyError, e:
                raise AssertionError, "Missing '%s' cvd_info field"\
                    % (tag,)

        return '<cvd_info>%s</cvd_info>' % (xml_string,)


class Transaction(object):
    """
    This class creates a transaction object which is meant to be used
    with a Server objects' do_request() method.

    There are a lot of transaction types and parameters required for
    each.  For details either read the source for this class or review
    the Moneris API documentation.

    >>> txn = Transaction(type='purchase', cust_id='your_id',
    ...                   amount='0.99', pan='4242424242424242',
    ...                   expdate='1109', crypt_type='7')
    """

    # AFAIK, we use this data-structure since dicts don't maintain
    # order.  The API xml spec is sensitive to order, so this API
    # interface must go to lengths to ensure that order.
    _txn_types = dict(
        purchase=['order_id', 'cust_id','amount',
                  'pan', 'expdate', 'crypt_type'],
        idebit_purchase=['order_id', 'cust_id','amount', 'idebit_track2'],
        idebit_refund=['order_id', 'amount', 'txn_number' ],
        purchase_reversal=['order_id', 'amount' ],
        refund_reversal=['order_id', 'amount' ],
        refund=['order_id', 'amount', 'txn_number', 'crypt_type'],
        ind_refund=['order_id','cust_id', 'amount','pan',
                    'expdate', 'crypt_type'],
        preauth=['order_id','cust_id','amount','pan', 'expdate', 'crypt_type'],
        completion=['order_id', 'comp_amount','txn_number', 'crypt_type'],
        purchasecorrection=['order_id', 'txn_number', 'crypt_type'],
        forcepost=['order_id','cust_id', 'amount','pan','expdate',
                   'auth_code','crypt_type'],
        opentotals=['ecr_number'],
        batchclose=['ecr_number'],
        batchcloseall=[],
        cavv_purchase=['order_id','cust_id', 'amount', 'pan',
                       'expdate', 'cavv'],
        cavv_preauth=['order_id','cust_id', 'amount', 'pan',
                      'expdate', 'cavv'],
        recur_update=['order_id', 'cust_id', 'pan', 'expdate', 'recur_amount',
                      'add_num_recurs', 'total_num_recurs', 'hold',
                      'terminate'],
        res_add_cc=['cust_id', 'phone', 'email', 'note', 'pan', 'expdate',
                    'crypt_type'],
        res_update_cc=['data_key', 'cust_id', 'phone', 'email', 'note', 'pan',
                       'expdate', 'crypt_type'],
        res_delete=['data_key'],
        res_lookup_full=['data_key'],
        res_lookup_masked=['data_key'],
        res_get_expiring=[],
        res_purchase_cc=['data_key', 'order_id', 'cust_id', 'amount',
                         'crypt_type'],
        res_preauth_cc=['data_key', 'order_id', 'cust_id', 'amount',
                        'crypt_type'],
        res_ind_refund_cc=['data_key', 'order_id', 'cust_id', 'amount',
                           'crypt_type'],
        res_iscorporatecard=['data_key'])

    def __init__(self, **req_data):
        try:
            txn_type = req_data.get('type')
        except KeyError, e:
            raise ValueError, "Must specify a transaction type"

        if txn_type not in self._txn_types.keys():
            raise ValueError, "%s is not a valid transaction type"\
                % (txn_type,)

        self.txn_type = txn_type
        self.req_data = req_data
        self.recur = None
        self.cust_info = None
        self.avs_info = None
        self.cvd_info = None

    def _to_xml(self):
        # Here we are generating the xml for the request to make sure
        # the tags appear in the order Moneris' API expects them in.
        # The user should never have to call this, just the Server
        # when generating a request.
        xml_string = ''
        for tag in self._txn_types[self.txn_type]:
            try:
                xml_string += '<%s>%s</%s>' % (tag, self.req_data[tag], tag)
            except KeyError, e:
                raise KeyError, "%s is not a valid field for '%s' transaction"\
                    % (tag, self.txn_type)
        if self.recur:
            xml_string += self.recur._to_xml()

        if self.cust_info:
            xml_string += self.cust_info._to_xml()

        if self.avs_info:
            xml_string += self.avs_info._to_xml()

        if self.cvd_info:
            xml_string += self.cvd_info._to_xml()

        return '<%s>%s</%s>' % (self.txn_type,
                                xml_string,
                                self.txn_type)

    def add_recur(self, recur_unit, start_now, start_date,
                  num_recurs, period, recur_amount):
        mpg_recur = MpgRecur(recur_unit=recur_unit,
                             start_now=start_name,
                             start_date=start_date,
                             num_recurs=num_recurs,
                             period=period,
                             recur_amount=recur_amount)
        self.recur = mpg_recur

    def add_cust_info(self, email=None, instructions=None, shipping=None,
                      billing=None, item=None):
        cust_info = MpgCustInfo(email, instructions, shipping,
                                billing, item)
        self.cust_info = cust_info

    def add_avs_info(self, street_num, street_name, zipcode):
        avs_info = MpgAvsInfo(avs_street_number=street_num,
                              avs_street_name=street_name,
                              avs_zipcode=zipcode)
        self.avs_info = avs_info

    def add_cvd_info(self, indicator, value):
        cvd_info = MpgCvdInfo(cvd_indicator=indicator,
                              cvd_value=value)
        self.cvd_info = cvd_info


class Response(object):
    """
    This object naively assigns the keys and values of the returned
    dictionary as attributes on itself.  It contains the response
    values from a completed transaction and should be checked for
    success, failure, and other erroneous conditions in the receipt.
    """

    # This class could have a better interface, at least for
    # documentation's sake.

    def __init__(self, response_xml):
        self._response_xml = response_xml
        self._response_dict = xml_to_dict(self._response_xml)
        for k, v in self._response_dict.items():
            setattr(self, k, v)

    @property
    def is_null(self):
        if self.recipt['ResponseCode'] == 'null':
            return True
        else:
            return False


class Server(object):
    """
    This object handles generating a request to the Moneris server and
    returns a Response object.  Your primarily do this by calling
    do_response() on an instantiated Server object.
    """

    def __init__(self, store_id, api_token, protocol=None, host=None,
                 port=None, path=None, timeout=None):
        self.store_id = store_id
        self.api_token = api_token
        self._protocol = protocol
        self._host = host
        self._port = port
        self._path = path
        self._timeout = timeout
        self._version = __version__

    @property
    def _url(self):
        path = self._path[1:] if self._path.startswith('/') else self._path
        host = self._host[:-1] if self._host.endswith('/') else self._host
        url = "%s://%s:%s/%s" % (self._protocol,
                                 host,
                                 self._port,
                                 path)
        return url

    def _to_xml(self, transaction):
        """ Generates the top-level XML to be sent in a request """
        header = "<?xml version=\"1.0\"?>"\
            + "<request>"\
            + "<store_id>" + self.store_id + "</store_id>"\
            + "<api_token>" + self.api_token + "</api_token>"
        body = transaction._to_xml()
        return header + body + "</request>"

    def do_request(self, transaction):
        """
        Generates the XML and intitiates a request transaction with
        the Moneris server.  Note that urllib may throw exceptions if
        it cannot talk to the server, so be sure to catch those when
        calling this method.

        Returns a Response object.
        """
        request = urllib2.Request(self._url)
        request_xml = self._to_xml(transaction)

        if self._protocol == 'http':
            handler = urllib2.HTTPHandler()
        elif self._protocol == 'https':
            handler = urllib2.HTTPSHandler()
        else:
            raise ValueError, "'%s' is not a supported protocol"\
                % (self._protocol,)

        opener = urllib2.build_opener(handler)
        opener.add_headers = [('User-agent', self._version)]
        urllib2.install_opener(opener)

        data = urllib2.urlopen(request, request_xml)
        
        resp_xml = ''.join(data.readlines())
        resp = Response(resp_xml)
        return resp


if __name__ == '__main__':
    import sys
    import hashlib
    import time

    store_id = sys.argv[1]
    api_token = sys.argv[2]
    order_id = hashlib.md5(str(time.time())).hexdigest()

    conn_params = dict(
        protocol='https',
        host='esqa.moneris.com',
        port='443',
        path='/gateway2/servlet/MpgRequest',
        timeout='60')

    request_data = dict(
        type='purchase',
        order_id=order_id,
        cust_id='your_cust_id',
        amount='0.99',
        pan='4242424242424242',
        expdate='1109',
        crypt_type='7')

    txn = Transaction(**request_data)
    txn.add_avs_info(123, 'Maple Street', 'M2M2M2')

    server = Server(store_id, api_token, **conn_params)
    print server._to_xml(txn)
    resp = server.do_request(txn)
    
    print resp.receipt
