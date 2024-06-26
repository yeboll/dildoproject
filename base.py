import os
from importlib import import_module
modules_path = 'modules/'

class Strategy():

    def load_strategy_modules(self, mod_cfg):
        modules = []
        for module_name in mod_cfg.keys():
            try:
                mod = modules_path + module_name
                mod = mod.replace('/', '.')
                module = import_module(mod)
                class_ = getattr(module, module_name)
                module_obj = class_(mod_cfg[module_name])
                modules.append({'name' : module_name, 
                                'obj' : module_obj})
            except:
                pass
        return modules


    # сюда передаем конфиги, и стратегия
    # должна сама автоматически подгрузить
    # необходимые модули для анализа свеч
    def __init__(self, conf):
        self.sol = {
            'action' : None,
            'tp' : None,
            'sl' : None,
            'deadline' : None,
            'log' : []
        }
        self.modules = self.load_strategy_modules(conf)
        self.conf = conf

    # с использованием всех сконфигурированных
    # модулей сформировать торговое решение и вернуть
    # его в self.sol, в data - данные, на основе которых
    # было принято это решение
    def decide(self, data):
        return (self.sol, data) 

class Module():
    def __init__(self, conf):
        self.conf = conf

    # в data добавляем необходимые колонки
    # которые будут использоваться стратегией
    # для формирования торгового решения
    def analize(self, data):
        return data



