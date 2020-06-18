from virtual_tabletop.Connections import FirebaseConnector

class VT:
    def __init__(self):
        self.source = FirebaseConnector.Connector('key.json')