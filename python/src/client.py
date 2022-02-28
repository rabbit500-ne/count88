
#------------------------------------------------
# クライアント
#------------------------------------------------
class Calc_contents():
    def __init__(self):
        contents = None

    def set_contents(self, str):
        pass

    def run_contents(self):
        pass

class NetworkClient():
    def __init__(self):
        self.url = "--"
        self.port = "--"
        self.req = "--"

    def request(self):
        return responce

    def answer(self,ans):
        pass


class Client(Calc_contents, NetworkClient):
    def __init__(self):
        Calc_contents.__init__(self) # これであってる？
        NetworkClient.__init__(self)

    def req_formula(self):
        responce = self.request()
        self.calc()

    def calc(self):
        self.set_contesnts(responce)
        ans = self.run_contents()
        self.answer(ans)
        