import datetime
import pandas as pd
class DashUtilities:
    __instance__ = None
    def __init__(self):
        if DashUtilities.__instance__ is None:
            DashUtilities.__instance__ = self
        else:
            pass
    @staticmethod
    def getInstance():
        if not DashUtilities.__instance__:
            DashUtilities()
        return DashUtilities.__instance__
    
    
    
    
    
    
    
    
    
    @staticmethod
    def generateMarks(input):
        ret = {}
        if isinstance(input, list):
            for x in input:
                ret[x] = {'label': str(x)}
        elif isinstance(input, dict):
            for key, value in input.items():
                ret[key] = {'label': str(value)}
        return ret
    
    @staticmethod
    def generateDropdownList(input = None, all=None,none=None):
        ret=[]
        if(input is None or (input is not None and len(input)<=0)):
            ret.append({'label': 'Empty', 'value': ''})
            return ret
        if(none is not None):
            ret.append({'label': 'None', 'value': none})
        elif(all is not None):
            ret.append({'label': 'All', 'value': all})
        if(isinstance(input, list)):
            for v in input:
                ret.append({'label': v, 'value': v})
        elif(isinstance(input, dict)):
            for key, value in input.items():
                ret.append({'label': key, 'value': value})
        return ret
    @staticmethod
    def generateData(x = [],y = [], type = 'line', name = ''):
        ret = []
        if isinstance(y, pd.DataFrame) and len(y.columns)>1:
            for column in y:
                ret.append(DashUtilities.__generateRawData__(x,y[column],type[column] if isinstance(type, dict) else type,name[column] if isinstance(name, dict) else column))
        else:
            ret.append(DashUtilities.__generateRawData__(x,y,type,name))
        return ret
    @staticmethod
    def __generateRawData__(x=[],y=[],type='line',name=''):
        return {'x': x, 'y': y, 'type': type, 'name': name}
    @staticmethod
    def generateSingleData(x=[],y=[],type='line',name=''):
        return __generateRawData__(x,y,type,name)
    @staticmethod
    def generateFigure(data = [], title = "", layout = None):
        if(layout is None):
            layout = {
                'title': title
            }
        return {
            'data':data,
            'layout': layout
        }
    @staticmethod
    def emptyFigure():
        return DashUtilities.generateFigure(layout = {})
    @staticmethod
    def placeholderFigure():
        return DashUtilities.generateFigure(data = DashUtilities.generateData([2,3,4,5,6],[3,6,6,7,9]))