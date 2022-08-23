import requests
import json

class RpcError(Exception):
    """Specifically created for error-handling of the BitcoiCore-API
    if thrown, check for errors like this:
    try:
        rpc.does_not_exist()
    except RpcError as rpce:
        assert rpce.error_code == -32601
        assert rpce.error_msg == "Method not found"
    See for error_codes https://github.com/bitcoin/bitcoin/blob/v0.15.0.1/src/rpc/protocol.h#L32L87
    """

    def __init__(self, message, response):
        super(Exception, self).__init__(message)
        self.status_code = 500  # default
        try:
            self.status_code = response.status_code
            error = response.json()
        except Exception as e:
            # it's a dict already
            error = response
        try:
            self.error_code = error["error"]["code"]
            self.error_msg = error["error"]["message"]
        except Exception as e:
            self.error = "UNKNOWN API-ERROR:%s" % response.text


class BitcoinRPC:

    def __init__(
        self,
        user="bitcoin",
        password="secret",
        host="127.0.0.1",
        port=8332,
        protocol="http",
        path="",
        timeout=None,
        session=None,
        **kwargs,
    ):
        path = path.replace("//", "/")  # just in case
        self.user = user
        self._password = password
        self.port = port
        self.protocol = protocol
        self.host = host
        self.path = path
        self.timeout = timeout
        self.r = None
        # session reuse speeds up requests
        if session is None:
            self._create_session()
        else:
            self.session = session

    def _create_session(self):
        session = requests.Session()
        session.auth = (self.user, self.password)
        # check if we need to connect over Tor
        self.session = session

    def wallet(self, name=""):
        return BitcoinRPC(
            user=self.user,
            password=self.password,
            port=self.port,
            protocol=self.protocol,
            host=self.host,
            path="{}/wallet/{}".format(self.path, name),
            timeout=self.timeout,
            session=self.session,
        )

    def mine(self, n=1):
        return self.generatetoaddress(n, self.getnewaddress())

    @property
    def url(self):
        return "{s.protocol}://{s.host}:{s.port}{s.path}".format(s=self)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
        self._create_session()

    def test_connection(self):
        """ returns a boolean depending on whether getblockchaininfo() succeeds """
        try:
            self.getblockchaininfo()
            return True
        except:
            return False

    def multi(self, calls: list, **kwargs):
        """Makes batch request to Core"""
        headers = {"content-type": "application/json"}
        payload = [
            {
                "method": method,
                "params": args if args != [None] else [],
                "jsonrpc": "2.0",
                "id": i,
            }
            for i, (method, *args) in enumerate(calls)
        ]
        timeout = self.timeout
        if "timeout" in kwargs:
            timeout = kwargs["timeout"]
        url = self.url
        if "wallet" in kwargs:
            url = url + "/wallet/{}".format(kwargs["wallet"])
        r = self.session.post(
            url, data=json.dumps(payload), headers=headers, timeout=timeout
        )
        self.r = r
        if r.status_code != 200:
            raise RpcError(
                "Server responded with error code %d: %s" % (r.status_code, r.text), r
            )
        r = r.json()
        return r

    def __getattr__(self, method):
        def fn(*args, **kwargs):
            r = self.multi([(method, *args)], **kwargs)[0]
            if r["error"] is not None:
                raise RpcError("Request error: %s" % r["error"]["message"], r)
            return r["result"]

        return fn


if __name__ == "__main__":

    rpc = BitcoinRPC(
        "bitcoin", "secret", port=18443
    )
    print(rpc.url)
    print(rpc.getmininginfo())
    print(rpc.listwallets())

    ##### WORKING WITH WALLETS #########

    # print(rpc.getbalance(wallet=""))
    # or
    w = rpc.wallet("")  # will load default wallet.dat
    print(w.url)
    print(w.getbalance())  # now you can run -rpcwallet commands
