class Module():
    def __init__(self, conf):
        self.conf = conf
        self.sol = {
            'action' : None,
            'tp' : None, 
            'sl' : None,
            'deadline' : None,
            'log' : []
        }
    
    def decide(self, data):
        ...
