

from gear.iocontract import TermSet, Var
from gear.polyhedralterm import PolyhedralTerm, PolyhedralTermSet
import logging
from sympy.parsing.sympy_parser import parse_expr
import sympy as sympy
import pytest

def to_pt(str_rep):
    expr = parse_expr(str_rep)
    assert isinstance(expr, sympy.core.relational.LessThan)
    constant = expr.args[1]
    variables = {}
    for k,v in expr.args[0].as_coefficients_dict().items():
        if k == 1:
            pass
        elif isinstance(k,sympy.core.symbol.Symbol):
            variables[str(k)] = v
        elif isinstance(k,sympy.core.mul.Mul):
            if isinstance(k.args[1], k,sympy.core.symbol.Symbol):
                variables[str(k.args[1])] = k.args[0]
            elif isinstance(k.args[0], k,sympy.core.symbol.Symbol):
                variables[str(k.args[0])] = k.args[1]
        else:
            raise ValueError
    return PolyhedralTerm(variables, constant)

def to_pts(str_rep_list):
    terms = [to_pt(str_rep) for str_rep in str_rep_list]
    return PolyhedralTermSet(set(terms))

def test_polyhedral_abduce_1():
    x = Var('x')
    # the context cannot simplify or transform the reference
    reference = to_pts(["2*x <= 4"])
    context = to_pts(["2*x <= 5"])
    expected = reference.copy()
    vars_elim = {x}
    reference = reference.abduce_with_context(context, vars_elim)
    assert(reference.terms == expected.terms)

def test_polyhedral_abduce_2():
    x = Var('x')
    # the context can simplify but not transform the reference
    reference = to_pts(["2*x <= 4"])
    context = to_pts(["2*x <= 3"])
    expected = to_pts([])
    vars_elim = {x}
    reference = reference.abduce_with_context(context, vars_elim)
    assert(reference.terms == expected.terms)

def test_polyhedral_abduce_3():
    # the context can transform the reference
    x = Var('x')
    y = Var('y')
    reference = to_pts(["x + y <= 4"])
    context = to_pts(["y <= 10"])
    expected = to_pts(["x <= -6"])
    vars_elim = {y}
    reference = reference.abduce_with_context(context, vars_elim)
    assert(reference.terms == expected.terms)

def test_polyhedral_abduce_4():
    # a term that cannot be simplified
    x = Var('x')
    reference = to_pts(["x <= -1"])
    context = to_pts(["-x + y <= 0"])
    expected = to_pts(["x <= -1"])
    vars_elim = {x}
    reference = reference.abduce_with_context(context, vars_elim)
    assert(reference.terms == expected.terms)

def test_polyhedral_abduce_5():
    # a term that can be simplified with one element of the context
    x = Var('x')
    reference = to_pts(["x <= -1"])
    context = to_pts(["x - y <= 0"])
    expected = to_pts(["y <= -1"])
    vars_elim = {x}
    reference = reference.abduce_with_context(context, vars_elim)
    assert(reference.terms == expected.terms)

def test_polyhedral_abduce_6():
    # a term that can be simplified with one element of the context
    x = Var('x')
    z = Var('z')
    reference = to_pts(["x <= -1"])
    context = to_pts(["x - y <= 0", "-z + x <= 0"])
    expected = to_pts(["y <= -1"])
    vars_elim = {x, z}
    reference = reference.abduce_with_context(context, vars_elim)
    assert(reference.terms == expected.terms)


def test_simplify_1():
    reference = to_pts(["-1/2*i <= -3/2","3*i <= 1", "-1*i <= 2", "1*i <= 2"])
    expected = to_pts(["-1/2*i <= -3/2","3*i <= 1"])
    with pytest.raises(ValueError):
        reference.simplify()
    