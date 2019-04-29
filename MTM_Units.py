#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        MTM_Units PYTHON 3.5
# Purpose:     Units system to any purpouse
#
# Author:      Miguel Tejada Molina
#
# Created:     07/12/2016
# Copyright:
# email:       tejada.miguel@gmail.com
#v0.2; 170317; MTEJADA; Added similarUnits
#v0.3; 170824; MTEJADA; Added ksi, supressed lum
#v0.4; 170824; MTEJADA; added check for long number
#v0.5; 170918; MTEJADA; Modified year and time
#v0.6; 170925; MTEJADA; Added bool op (nonzero)
#v0.7; 171001; MTEJADA; Added unit.plus at unit creation when is isolated
#v0.8; 171016; MTEJADA; Added constant as __all__ values
#v0.8; 171111; MTEJADA; Modified miles units
#v1.0; 171211; MTEJADA; Agregado mmHg
#v1.1; 180205; MTEJADA; Port to PYTHON 3.5
#v1.2; 180214; MTEJADA; Implemented JSON
#-------------------------------------------------------------------------------
from math import *
from collections import OrderedDict
import sys
import json

__author__ = "Miguel Tejada"
__version__ = "1.2"
__email__ = "tejada.miguel@gmail.com"
__license__ = "GPL"
__all__ = ["metricPrefix","unitDict","Unit","constant"]

metricPrefix = OrderedDict([('a',1E-18), ('f',1E-15), ('p',1E-12), ('n',1E-9), ('u',1E-6),
     ('m',1E-3),('c',1E-2),('d',1E-1),('da',1E1),('h',1E2),('k',1E3),('M',1E6),('G',1E9),
     ('T',1E12),('P',1E15),('E',1E18)])

unitDict = OrderedDict([
            ('m',[1,0,0,0,0,0,0,1]),
            ('g',[0,1,0,0,0,0,0,1]),
            ('s',[0,0,1,0,0,0,0,1]),
            ('A',[0,0,0,1,0,0,0,1]),
            ('K',[0,0,0,0,1,0,0,1]),
            ('mol',[0,0,0,0,0,1,0,1]),
            ('cd',[0,0,0,0,0,0,1,1]), #no alterar este orden
            #no basicos LONGITUD
            ('hectare',[2,0,0,0,0,0,0,10000]),
            ('litre',[3,0,0,0,0,0,0,0.001]),
            ('in',[1,0,0,0,0,0,0,0.0254]),
            ('ft',[1,0,0,0,0,0,0,0.3048]),
            ('yd',[1,0,0,0,0,0,0,0.9144]),
            ('mi',[1,0,0,0,0,0,0,1609.344]),
            #no basicos TIEMPO
            ('Hz',[0,0,-1,0,0,0,0,1]),
            ('year',[0,0,1,0,0,0,0,365*24.*3600]),
            ('week',[0,0,1,0,0,0,0,7*24.*3600]),
            ('day',[0,0,1,0,0,0,0,24.*3600]),
            ('minute',[0,0,1,0,0,0,0,60.]),
            ('hour',[0,0,1,0,0,0,0,3600.]),
            #no basicos PESO
            ('tonne',[0,1,0,0,0,0,0,1000000.]),
            ('oz',[0,1,0,0,0,0,0,28.349523125]),
            ('lb',[0,1,0,0,0,0,0,453.59237]),
            #no basicos FUERZA
            ('N',[1,1,-2,0,0,0,0,1000.]),
            ('kgf',[1,1,-2,0,0,0,0,9806.65]),
            ('lbf',[1,1,-2,0,0,0,0,4448.222]),
            ('dyn',[1,1,-2,0,0,0,0,0.01]),
            ('pdl',[1,1,-2,0,0,0,0,138.255]),
            #no basicos TEMPERATURA
            ('Celsius',[0,0,0,0,1,0,0,1,+273.15]),    #[m,g,s,A,K,mol,cd]
            ('Fahrenheit',[0,0,0,0,1,0,0,5/9,+255.37222]),
            #no basicos PRESION
            ('Pa',[-1,1,-2,0,0,0,0,1000.]),
            ('bar',[-1,1,-2,0,0,0,0,100000000.]),
            ('psi',[-1,1,-2,0,0,0,0,6894760.]),
            ('ksi',[-1,1,-2,0,0,0,0,6894760000.]),
            ('mmHg',[-1,1,-2,0,0,0,0,133322.3684]),
            ('atm',[-1,1,-2,0,0,0,0,101325000.]),
            #no basicos ENERGIA
            ('J',[2,1,-2,0,0,0,0,1000.]),
            ('eV',[2,1,-2,0,0,0,0,1.60217553e-11]),
            ('cal',[2,1,-2,0,0,0,0,1000*4.184]),
            ('BTU',[2,1,-2,0,0,0,0,1055.056*1000.]),
            #no basicos POTENCIA
            ('W',[2,1,-3,0,0,0,0,1000]),
            #no basicos ELECTRICIDAD
            ('C',[0,0,1,1,0,0,0,1]),
            ('V',[2,1,-3,-1,0,0,0,1000]),
            ('F',[-2,-1,4,2,0,0,0,0.001]),
            ('Ohm',[2,1,-3,-2,0,0,0,1000]),
            ('Siemens',[-2,-1,3,2,0,0,0,0.001]),
            ('Wb',[2,1,-2,-1,0,0,0,1000]),
            ('T',[0,1,-2,-1,0,0,0,1000]),
            ('H',[2,1,-2,-2,0,0,0,1000]),
            ('lx',[-2,0,0,0,0,0,1,1]),
            ('kat',[0,0,-1,0,0,1,0,1])
             ])

class _MetaUnit_(type):
    def __getattr__(self,name):
        value, un = Unit.__parseUnits__(name)
        return Unit(value,un)

class Unit(object):
    """Object to keep physical units. Read the units name from the 'unitDict' dictionary
    and the 'metricPrefix' dictionary
    The objects created may be combined with +,-,*,/
    All the units will be stored in the SI, and return the value by default in
    the units pre-defined.
    """
    __metaclass__ = _MetaUnit_
    def __init__(self,value,unit=None):
        """Unit instance:
        Arg1 (int,float,Unit,str): value
            - value (int,float): magnitude of unit. Needs second arg as unit.
            - value (Unit): return a copy of passed unit
            - value (str): Parse the string and old them
        Arg2 (None,str,Unit,list,tuple,_basicUnit): unit
            - Parse and keeps units as _basicUnit_ type
        """
        if isinstance(value,Unit):
            myvalue = value.value*value.unit.coef
            myunit = _basicUnit_(value.unit)
            myunit.coef = 1
        elif isinstance(value,str):
            val,un = value.split(" ")
            myvalue = eval(val)
            valun,myunit = Unit.__parseUnits__(un)
            myvalue = eval(val)*valun
            if len(myunit._un) > 8:
                myvalue = myvalue + myunit._un[8]
                myunit._un = myunit._un[:8]
        elif isinstance(value,(int,float)):
            myvalue = value
            if not unit: raise IOError('Missing units')

        if unit:
            if isinstance(unit, str):
                newval,myunit = Unit.__parseUnits__(unit)
                myvalue = myvalue * newval + myunit.plus
            elif isinstance(unit,(list,tuple)) and len(unit) >= 8:
                myunit = _basicUnit_(unit)
                myvalue *= myunit.coef + myunit.plus
                myunit.coef = 1
            elif isinstance(unit,Unit):
                myvalue *= unit.unit.coef + unit.unit.plus
                myunit = _basicUnit_(unit.unit)
                myunit.coef = 1
            elif isinstance(unit,_basicUnit_):
                myvalue *= unit.coef + unit.plus
                myunit = _basicUnit_(unit)
                myunit.coef = 1
            else:
                raise IOError("Algo ha fallado con " + str(value) + str(unit))
        self.value = myvalue
        self.unit = myunit

    def getValueAs(self,strunit):
        """Return the value in the units passed as arg.
        """
        valor = self.value
        newval = 1
        unidad = None
        if isinstance(strunit, str):
            newval,unidad = Unit.__parseUnits__(strunit)
            valor /= newval
        elif isinstance(strunit,(list,tuple)) and len(strunit) >= 8:
            unidad = _basicUnit_(strunit)
        elif isinstance(strunit,Unit):
            unidad = strunit.unit
        else:
            raise IOError('Algo ha fallado con ' + strunit + ' type ' + str(type(strunit)))
        if unidad != self.unit:
            raise ValueError(strunit,' not compatible units')
            return None
        valor *= self.unit.coef/unidad.coef
        valor -= unidad.plus/newval
        return valor

    def getBasicRepr(self):
        "return value in SI"
        basicunits = unitDict.keys()[:7]
        strupper = ''
        strlower = ''
        for i in range(7):
            if self.unit[i] > 0:
                if strupper: strupper += '*'
                strupper += basicunits[i]
                if self.unit[i] > 1:
                    strupper = strupper + '**' + str(self.unit[i])
            elif self.unit[i] < 0:
                if strlower: strlower += '*'
                strlower += basicunits[i]
                if abs(self.unit[i]) > 1:
                    strlower = strlower + '**' + str(abs(self.unit[i]))
        strexit = str(self.value) + " " + strupper
        if strlower: strexit = strexit + "/" + strlower
        return strexit

    @staticmethod
    def listOfUnits():
        return unitDict.keys()

    @staticmethod
    def listOfPrefix():
        return metricPrefix.keys()

    def __repr__(self):
        unit = str(self.unit)
        value = self.value
        if unit in unitDict.keys():
            value = value/unitDict[unit][7]
        return str(value) + " " + unit

    def __str__(self):
        unit = str(self.unit)
        value = self.value
        if unit in unitDict.keys():
            value = value/unitDict[unit][7]
        return str(value) + " " + unit

    def __lt__(self,other):
        if not isinstance(other,Unit) or self.unit != other.unit: raise ValueError(other,'Not compatible units')
        if self.value < other.value: return True
        return False

    def __le__(self,other):
        if not isinstance(other,Unit) or self.unit != other.unit: raise ValueError(other,'Not compatible units')
        if self.value <= other.value: return True
        return False

    def __gt__(self,other):
        if not isinstance(other,Unit) or self.unit != other.unit: raise ValueError(other,'Not compatible units')
        if self.value > other.value: return True
        return False

    def __ge__(self,other):
        if not isinstance(other,Unit) or self.unit != other.unit: raise ValueError(other,'Not compatible units')
        if self.value >= other.value: return True
        return False

    def __eq__(self,other):
        if not isinstance(other,Unit) or self.unit != other.unit: raise ValueError(other,'Not compatible units')
        if self.value == other.value: return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)


    def __add__(self,other):
        if isinstance(other,Unit):
            if not self.unit == other.unit:
                raise ValueError(other,'Not compatible value')
                return None
            valor = self.value+other.value
            unit = _basicUnit_(self.unit)
            return Unit(valor,unit)
        else:
            raise ValueError(other,'needs a physicall dimension')

    def __sub__(self,other):
        if not isinstance(other,Unit) or self.unit != other.unit: raise ValueError(other,'Not compatible units')
        valor = self.value - other.value
        return Unit(valor,self.unit)

    def __mul__(self,other):
        if isinstance(other,Unit):
            valor = self.value*other.value
            unit = _basicUnit_(self.unit)*other.unit
        elif isinstance(other,(int,float)):
            valor = self.value*other
            unit = self.unit
        return Unit(valor,unit)

    def __rmul__(self,other):
        if isinstance(other,Unit):
            valor = self.value*other.value
            unit = self.unit*other.unit
        elif isinstance(other,(int,float)):
            valor = self.value*other
            unit = self.unit
        return Unit(valor,unit)

    def __div__(self,other):
        if isinstance(other,Unit):
            valor = self.value/other.value
            unit = self.unit/other.unit
        elif isinstance(other,(int,float)):
            valor = self.value/other
            unit = self.unit
        else:
            raise ValueError(other)
        return Unit(valor,unit)

    def __rdiv__(self,other):
        if isinstance(other,Unit):
            valor = other.value/self.value
            unit = other.unit/self.unit
        elif isinstance(other,(int,float)):
            valor = float(other)/self.value
            unit = self.unit**-1
        else:
            raise ValueError(other)
        return Unit(valor,unit)

    def __truediv__(self,other):
        if isinstance(other,Unit):
            valor = self.value/other.value
            unit = self.unit/other.unit
        elif isinstance(other,(int,float)):
            valor = self.value/other
            unit = self.unit
        else:
            raise ValueError(other)
        return Unit(valor,unit)

    def __rtruediv__(self,other):
        if isinstance(other,Unit):
            valor = other.value/self.value
            unit = other.unit/self.unit
        elif isinstance(other,(int,float)):
            valor = float(other)/self.value
            unit = self.unit**-1
        else:
            raise ValueError(other)
        return Unit(valor,unit)


    def __pow__(self,module):
        valor = self.value**module
        unit = self.unit**module
        return Unit(valor,unit)

    def __neg__(self):
        unit = Unit(self)
        unit.valor = -unit.valor
        return unit

    def __abs__(self):
        unit= Unit(self)
        unit.valor = abs(unit.valor)
        return unit

    def truth(self):
        return True if self.value else False

    def __bool__(self):
        return True if self.value else False

    def __nonzero__(self):
        return True if self.value else False

    @staticmethod
    def similarUnits(unitname):
        "Get all similar units"
        valor, unidad = Unit.__parseUnits__(unitname)
        resultado = []
        for key,value in unitDict.items():
            if key != unitname and unidad == _basicUnit_(value):
                resultado.append(key)
        return resultado

    @staticmethod
    def __parseUnits__(unitstring):
        'Funcion que descompone la unidad en partes diverenciadas'
        import re
        splitphrase = re.compile(r'[;|\(|\)|\/|\**|\*|\s]')
        partes = splitphrase.split(unitstring)
        partes = [x for x in partes if (not x.isdigit() and x)]
        valores = {}
        unidades = {}
        for unidad in partes:
            if unidad[0] in metricPrefix.keys() and unidad[1:] in unitDict.keys():
                valores[unidad] = metricPrefix[unidad[0]]
                unidades[unidad] = unitDict[unidad[1:]]
            elif unidad[0:2] in metricPrefix.keys() and unidad[2:] in unitDict.keys():
                valores[unidad] = metricPrefix[unidad[0:2]]
                unidades[unidad] = unitDict[unidad[2:]]
            elif unidad in unitDict.keys():
                valores[unidad] = 1
                unidades[unidad] = unitDict[unidad]
            else:
                raise ValueError(unitstring)
        newstring = ""
        i = 0
        j = 0
        while i < len(unitstring):
            if unitstring[i] in ['*','/','(',')'] or unitstring[i].isdigit():
                newstring += unitstring[i]
                i += 1
            else:
                newstring += '$$'+partes[j]+'$$'
                i += len(partes[j])
                j += 1
        valor = newstring
        unidad = newstring
        for un in partes:
            valor = valor.replace('$$' + un + '$$',str(valores[un]))
            unidad = unidad.replace('$$' + un + '$$', '_basicUnit_(' + str(unidades[un]) + ')')
        valor = eval(valor)
        unidad = eval(unidad)
        valor *= unidad.coef
        #valor += unidad.plus
        unidad.coef = 1
        return valor, unidad

    def __json__(self):
        return {'__jsoncls__':'MTM_Units:Unit.from_JSON','value':self.value,'unit':self.unit._un}

    @classmethod
    def from_JSON(cls,jsondict):
        value = jsondict['value']
        unit = _basicUnit_(jsondict['unit'])
        obj = cls(value,unit)
        return obj
class _basicUnit_(object):
    'establece las operaciones basicas para las cadenas de lista'
    def __init__(self,ulist):
        if isinstance(ulist,(tuple,list)) and len(ulist) >= 8:
            self._un = ulist
        elif isinstance(ulist,_basicUnit_):
            self._un = ulist._un

    def __mul__(self,other):
        un = [0]*8
        if isinstance(other,_basicUnit_):
            for i in range(7):
                un[i] = self._un[i]+other._un[i]
            un[7] = self._un[7]*other._un[7]
            return _basicUnit_(un)
        else:
            return un

    def __div__(self,other):
        un = [0]*8
        for i in range(7):
            un[i] = self._un[i]-other._un[i]
        un[7] = self._un[7]/other._un[7]
        return _basicUnit_(un)

    def __truediv__(self,other):
        un = [0]*8
        for i in range(7):
            un[i] = self._un[i]-other._un[i]
        un[7] = self._un[7]/other._un[7]
        return _basicUnit_(un)

    def __pow__(self,modulo):
        un = [0]*8
        for i in range(7):
            un[i] = self._un[i]*modulo
        un[7] = self._un[7]**modulo
        return _basicUnit_(un)

    def __eq__(self,other):
        if self._un[:7] == other._un[:7]:
            return True
        else: return False
    def __ne__(self,other):
        if self._un[:7] != other._un[:7]:
            return True
        else: return False

    @property
    def coef(self):
        return self._un[7]

    @coef.setter
    def coef(self,coef):
        self._un[7] = coef

    @property
    def plus(self):
        if len(self._un) > 8:
            return self._un[8]
        else:
            return 0

    @plus.setter
    def plus(self,value):
        if len(self._un) > 8:
            self._un[8] = value
        else:
            self._un.append(value)

    def __repr__(self):
        upper = ""
        lower = ""
        for key,value in unitDict.items():
            if value[:7] == self._un[:7]:
                return key
        for i in range(7):
            if self._un[i] != 0:
                lista = [0]*8
                lista[i] = 1
                lista[7] = 1
                letra = list(unitDict.keys())[list(unitDict.values()).index(lista)]
                if self._un[i] > 0:
                    if self._un[i] > 1:
                        letra += '**' + str(self._un[i])
                    if upper == "":
                        upper = letra
                    else:
                        upper += '*' + letra
                else:
                    if abs(self._un[i]) > 1:
                        letra += '**' + str(abs(self._un[i]))
                    if lower == "":
                        lower = letra
                    else:
                        lower += '*' + letra
        if not upper:
            return '1/' + lower

        if not lower:
            return upper
        else:
            if '*' in lower: lower = "(" + lower + ")"
            return upper + "/" + lower

    def __getitem__(self,key):
        return self._un[key]

a = Unit('0 g')

constant = {'mnu0': Unit('1.2566370614e-6 N/A**2'),
    'G': Unit('6.6742e-11 N*m**2/kg**2'),
    'h': Unit('6.6260693e-34 J*s'),
    'c': Unit('299792458 m/s'),
    'gravity': Unit('9.80665 m/s**2')}

if __name__ == '__main__':
    peso = Unit(16600,'mm**2')*Unit(2500,'kg/m**3')
    print(peso)
    valor = Unit(0,'Celsius')
    print(peso/valor)
