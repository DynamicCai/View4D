from lmfit import Parameters, minimize
from numpy import *

def havriliak_negami_permittivity(x, pars, comp):
    """2-d HNP: HNP(x, de{0}, logf0{1}, a{2}, b{3}, einf{4})"""
    de = pars[0]
    logf0 = pars[1]
    a = pars[2]
    b = pars[3]
    einf = pars[4]
    e = de / ( 1 + ( 1j * x / 10**logf0 )**a )**b + einf
    if comp == 'real':
        return e.real
    elif comp == 'imag':
        return -e.imag
    
def havriliak_negami_modulus(x, pars, comp):
    """2-d HNM: HNM(x, dM{0}, logtau0{1}, a{2}, b{3}, Ms{4})"""
    dM = pars[0]
    logf0 = pars[1]
    a = pars[2]
    b = pars[3]
    Ms = pars[4]
    modulus = Ms + dM - dM/( 1 + ( 1j * x / 10**logf0 )**a )**b
    if comp == 'real':
        return modulus.real
    elif comp == 'imag':
        return modulus.imag
    
def VFT(x, pars, comp):
    logf0 = pars[0]
    B = pars[1]
    T0 = pars[2]
    y = logf0 - log10(e) * B/(1000/x-T0)
    return y

def WLF(x, pars, comp):
    C1 = pars[0]
    C2 = pars[1]
    Tr = pars[2]
    y = -C1*(x-Tr)/(C2+x-Tr)
    return y
    
def HNP_move(x, y, xn, yn, de, logf0, a, b, einf):
    return [de*yn/y, logf0 + log10(xn/x), a, b, einf]

def HNM_move(x, y, xn, yn, dM, logf0, a, b, Ms):
    return [dM*yn/y, logf0 + log10(xn/x), a, b, Ms]

def VFT_move(x, y, xn, yn, logf0, B, T0):
    return [logf0, B, T0]

def WLF_move(x, y, xn, yn, C1, C2, Tr):
    return [C1, C2, Tr+xn-x]

functions = {
    'HNP': {
        'name': 'Havriliak Negami Permittivity',
        'pars': ['de', 'logf0', 'a', 'b', 'einf'],
        'value': [1,0,1,1,2],
        'limits': [(0,inf),(-inf,inf),(0,1),(0,1),(0,inf)],
        'function': havriliak_negami_permittivity,
        'move': HNP_move
    },
    'HNM': {
        'name': 'Havriliak Negami Modulus',
        'pars': ['dM', 'logf0', 'a', 'b', 'Ms'],
        'value': [1,0,1,1,2],
        'limits': [(0,inf),(-inf,inf),(0,1),(0,1),(0,inf)],
        'function': havriliak_negami_modulus,
        'move': HNM_move
    },
    'WLF': {
        'name': 'WLF equation',
        'pars': ['C1', 'C2', 'Tr'],
        'value': [1,1,273],
        'limits': [(0,inf),(0,inf),(0,inf)],
        'function': WLF,
        'move': WLF_move
    },
    'VFT': {
        'name': 'VFT equation',
        'pars': ['logf0', 'B', 'T0'],
        'value': [10,1000,150],
        'limits': [(-inf,inf),(-inf,inf),(-inf,inf)],
        'function': VFT,
        'move': VFT_move
    }
}
