class DummyConfig:

    class Subtensor:

        def __init__(self, chain_endpoint, network):

            self.chain_endpoint = chain_endpoint

            self.network = network



    def __init__(self):

        self.netuid = 13

        self.vpermit_rao_limit = 100_000_000_000

        self.chain_endpoint = "wss://finney.opentensor.ai:9944"

        self.network = "finney"

        self.subtensor = self.Subtensor(self.chain_endpoint, self.network)

        self.is_set = True





def get_config():

    return DummyConfig()


