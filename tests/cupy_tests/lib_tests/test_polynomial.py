import unittest

import pytest
import numpy

import cupy
import cupyx
from cupy import testing


@testing.parameterize(
    {'variable': None},
    {'variable': 'y'},
)
@testing.gpu
class TestPoly1dInit(unittest.TestCase):

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal()
    def test_poly1d_numpy_array(self, xp, dtype):
        a = numpy.arange(5, dtype=dtype)
        with cupyx.allow_synchronize(False):
            out = xp.poly1d(a, variable=self.variable)
        assert out.variable == (self.variable or 'x')
        return out.coeffs

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_cupy_array(self, xp, dtype):
        a = testing.shaped_arange((5,), xp, dtype)
        with cupyx.allow_synchronize(False):
            out = xp.poly1d(a, variable=self.variable)
        assert out.variable == (self.variable or 'x')
        return out.coeffs

    @testing.numpy_cupy_array_equal()
    def test_poly1d_list(self, xp):
        with cupyx.allow_synchronize(False):
            out = xp.poly1d([1, 2, 3, 4], variable=self.variable)
        assert out.variable == (self.variable or 'x')
        return out.coeffs

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_numpy_poly1d(self, xp, dtype):
        array = testing.shaped_arange((5,), numpy, dtype)
        a = numpy.poly1d(array)
        with cupyx.allow_synchronize(False):
            out = xp.poly1d(a, variable=self.variable)
        assert out.variable == (self.variable or 'x')
        return out.coeffs

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_numpy_poly1d_variable(self, xp, dtype):
        array = testing.shaped_arange((5,), numpy, dtype)
        a = numpy.poly1d(array, variable='z')
        with cupyx.allow_synchronize(False):
            out = xp.poly1d(a, variable=self.variable)
        assert out.variable == (self.variable or 'z')
        return out.coeffs

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_cupy_poly1d(self, xp, dtype):
        array = testing.shaped_arange((5,), xp, dtype)
        a = xp.poly1d(array)
        out = xp.poly1d(a, variable=self.variable)
        assert out.variable == (self.variable or 'x')
        return out.coeffs

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_cupy_poly1d_variable(self, xp, dtype):
        array = testing.shaped_arange((5,), xp, dtype)
        a = xp.poly1d(array, variable='z')
        out = xp.poly1d(a, variable=self.variable)
        assert out.variable == (self.variable or 'z')
        return out.coeffs

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_zero_dim(self, xp, dtype):
        a = testing.shaped_arange((), xp, dtype)
        with cupyx.allow_synchronize(False):
            out = xp.poly1d(a, variable=self.variable)
        assert out.variable == (self.variable or 'x')
        return out.coeffs

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_zero_size(self, xp, dtype):
        a = testing.shaped_arange((0,), xp, dtype)
        with cupyx.allow_synchronize(False):
            out = xp.poly1d(a, variable=self.variable)
        assert out.variable == (self.variable or 'x')
        return out.coeffs


@testing.gpu
class TestPoly1d(unittest.TestCase):

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_leading_zeros(self, xp, dtype):
        a = xp.array([0, 0, 1, 2, 3], dtype)
        return xp.poly1d(a).coeffs

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal()
    def test_poly1d_neg(self, xp, dtype):
        a = testing.shaped_arange((5,), xp, dtype)
        b = -xp.poly1d(a)
        return b.coeffs

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_order(self, xp, dtype):
        a = testing.shaped_arange((10,), xp, dtype)
        return xp.poly1d(a).order

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_order_leading_zeros(self, xp, dtype):
        a = xp.array([0, 0, 1, 2, 3, 0], dtype)
        return xp.poly1d(a).order

    @testing.for_signed_dtypes()
    @testing.numpy_cupy_allclose(rtol=1e-6)
    def test_poly1d_roots1(self, xp, dtype):
        a = xp.array([-3, -2.5, 3], dtype)
        out = xp.poly1d(a).roots
        # The current `cupy.roots` doesn't guarantee the order of results.
        return xp.sort(out)

    @testing.for_all_dtypes(no_bool=True)
    def test_poly1d_roots2(self, dtype):
        a = testing.shaped_arange((5,), cupy, dtype)
        with pytest.raises(NotImplementedError):
            cupy.poly1d(a).roots

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_getitem1(self, xp, dtype):
        a = testing.shaped_arange((10,), xp, dtype)
        with cupyx.allow_synchronize(False):
            return xp.poly1d(a)[-1]

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_getitem2(self, xp, dtype):
        a = testing.shaped_arange((10,), xp, dtype)
        with cupyx.allow_synchronize(False):
            return xp.poly1d(a)[5]

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_getitem3(self, xp, dtype):
        a = testing.shaped_arange((10,), xp, dtype)
        with cupyx.allow_synchronize(False):
            return xp.poly1d(a)[100]

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_getitem4(self, xp, dtype):
        a = xp.array([0, 0, 1, 2, 3, 0], dtype)
        with cupyx.allow_synchronize(False):
            return xp.poly1d(a)[2]

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_setitem(self, xp, dtype):
        a = testing.shaped_arange((10,), xp, dtype)
        b = xp.poly1d(a)
        with cupyx.allow_synchronize(False):
            b[100] = 20
        return b.coeffs

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal()
    def test_poly1d_setitem_leading_zeros(self, xp, dtype):
        a = xp.array([0, 0, 0, 2, 3, 0], dtype)
        b = xp.poly1d(a)
        with cupyx.allow_synchronize(False):
            b[1] = 10
        return b.coeffs

    @testing.for_all_dtypes()
    def test_poly1d_setitem_neg(self, dtype):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((10,), xp, dtype)
            b = xp.poly1d(a)
            with pytest.raises(ValueError):
                b[-1] = 20

    @testing.for_all_dtypes()
    def test_poly1d_get1(self, dtype):
        a1 = testing.shaped_arange((10,), cupy, dtype)
        a2 = testing.shaped_arange((10,), numpy, dtype)
        b1 = cupy.poly1d(a1, variable='z').get()
        b2 = numpy.poly1d(a2, variable='z')
        assert b1 == b2

    @testing.for_all_dtypes()
    def test_poly1d_get2(self, dtype):
        a1 = testing.shaped_arange((), cupy, dtype)
        a2 = testing.shaped_arange((), numpy, dtype)
        b1 = cupy.poly1d(a1).get()
        b2 = numpy.poly1d(a2)
        assert b1 == b2

    @testing.for_all_dtypes(no_bool=True)
    def test_poly1d_set(self, dtype):
        arr1 = testing.shaped_arange((10,), cupy, dtype)
        arr2 = numpy.ones(10, dtype=dtype)
        a = cupy.poly1d(arr1)
        b = numpy.poly1d(arr2, variable='z')
        a.set(b)
        assert a.variable == b.variable
        testing.assert_array_equal(a.coeffs, b.coeffs)

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_repr(self, xp, dtype):
        a = testing.shaped_arange((5,), xp, dtype)
        return repr(xp.poly1d(a))

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_str(self, xp, dtype):
        a = testing.shaped_arange((5,), xp, dtype)
        return str(xp.poly1d(a))


class Poly1dTestBase(unittest.TestCase):

    def _get_input(self, xp, in_type, dtype):
        if in_type == 'poly1d':
            return xp.poly1d(testing.shaped_arange((10,), xp, dtype) + 1)
        if in_type == 'ndarray':
            return testing.shaped_arange((10,), xp, dtype)
        if in_type == 'python_scalar':
            return dtype(5).item()
        if in_type == 'numpy_scalar':
            return dtype(5)
        assert False


@testing.gpu
@testing.parameterize(*testing.product({
    'func': [
        lambda x, y: x + y,
        lambda x, y: x - y,
    ],
    'type_l': ['poly1d', 'python_scalar'],
    'type_r': ['poly1d', 'ndarray', 'python_scalar', 'numpy_scalar'],
}))
class TestPoly1dArithmetic(Poly1dTestBase):

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal(accept_error=TypeError)
    def test_poly1d_arithmetic(self, xp, dtype):
        a1 = self._get_input(xp, self.type_l, dtype)
        a2 = self._get_input(xp, self.type_r, dtype)
        with cupyx.allow_synchronize(False):
            return self.func(a1, a2)


@testing.gpu
@testing.parameterize(*testing.product({
    'func': [
        lambda x, y: x + y,
        lambda x, y: x - y,
    ],
    'type_l': ['ndarray', 'numpy_scalar'],
    'type_r': ['poly1d'],
}))
class TestPoly1dArithmeticInvalid(Poly1dTestBase):

    @testing.for_all_dtypes()
    def test_poly1d_arithmetic_invalid(self, dtype):
        # CuPy does not support them because device-to-host synchronization is
        # needed to convert the return value to cupy.ndarray type.
        n1 = self._get_input(numpy, self.type_l, dtype)
        n2 = self._get_input(numpy, self.type_r, dtype)
        assert type(self.func(n1, n2)) is numpy.ndarray

        c1 = self._get_input(cupy, self.type_l, dtype)
        c2 = self._get_input(cupy, self.type_r, dtype)
        with pytest.raises(TypeError):
            self.func(c1, c2)


@testing.gpu
@testing.parameterize(*testing.product({
    'fname': ['polyadd', 'polysub'],
    'type_l': ['poly1d', 'ndarray', 'python_scalar', 'numpy_scalar'],
    'type_r': ['poly1d', 'ndarray', 'python_scalar', 'numpy_scalar'],
}))
class TestPoly1dRoutines(Poly1dTestBase):

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal(accept_error=TypeError)
    def test_poly1d_routine(self, xp, dtype):
        func = getattr(xp, self.fname)
        a1 = self._get_input(xp, self.type_l, dtype)
        a2 = self._get_input(xp, self.type_r, dtype)
        with cupyx.allow_synchronize(False):
            return func(a1, a2)


class UserDefinedArray:

    __array_priority__ = cupy.poly1d.__array_priority__ + 10

    def __init__(self):
        self.op_count = 0
        self.rop_count = 0

    def __add__(self, other):
        self.op_count += 1

    def __radd__(self, other):
        self.rop_count += 1

    def __sub__(self, other):
        self.op_count += 1

    def __rsub__(self, other):
        self.rop_count += 1


@testing.gpu
@testing.parameterize(*testing.product({
    'func': [
        lambda x, y: x + y,
        lambda x, y: x - y,
    ],
}))
class TestPoly1dArrayPriority(Poly1dTestBase):

    def test_poly1d_array_priority_greator(self):
        a1 = self._get_input(cupy, 'poly1d', 'int64')
        a2 = UserDefinedArray()
        self.func(a1, a2)
        assert a2.op_count == 0
        assert a2.rop_count == 1
        self.func(a2, a1)
        assert a2.op_count == 1
        assert a2.rop_count == 1


@testing.gpu
class TestPoly1dEquality(unittest.TestCase):

    def make_poly1d1(self, xp, dtype):
        a1 = testing.shaped_arange((4,), xp, dtype)
        a2 = xp.zeros((4,), dtype)
        b1 = xp.poly1d(a1)
        b2 = xp.poly1d(a2)
        return b1, b2

    def make_poly1d2(self, xp, dtype):
        a1 = testing.shaped_arange((4,), xp, dtype)
        a2 = testing.shaped_arange((4,), xp, dtype)
        b1 = xp.poly1d(a1)
        b2 = xp.poly1d(a2)
        return b1, b2

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_eq1(self, xp, dtype):
        a, b = self.make_poly1d1(xp, dtype)
        return a == b

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_eq2(self, xp, dtype):
        a, b = self.make_poly1d2(xp, dtype)
        return a == b

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_ne1(self, xp, dtype):
        a, b = self.make_poly1d1(xp, dtype)
        return a != b

    @testing.for_all_dtypes()
    @testing.numpy_cupy_equal()
    def test_poly1d_ne2(self, xp, dtype):
        a, b = self.make_poly1d2(xp, dtype)
        return a != b


@testing.gpu
@testing.parameterize(*testing.product({
    'fname': ['polyadd', 'polysub'],
    'shape1': [(), (0,), (3,), (5,)],
    'shape2': [(), (0,), (3,), (5,)]
}))
class TestPolyArithmeticShapeCombination(unittest.TestCase):

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal()
    def test_polyroutine(self, xp, dtype):
        func = getattr(xp, self.fname)
        a = testing.shaped_arange(self.shape1, xp, dtype)
        b = testing.shaped_arange(self.shape2, xp, dtype)
        with cupyx.allow_synchronize(False):
            return func(a, b)


@testing.gpu
@testing.parameterize(*testing.product({
    'fname': ['polyadd', 'polysub'],
}))
class TestPolyArithmeticDiffTypes(unittest.TestCase):

    @testing.for_all_dtypes_combination(names=['dtype1', 'dtype2'])
    @testing.numpy_cupy_array_equal(accept_error=TypeError)
    def test_polyroutine_diff_types_array(self, xp, dtype1, dtype2):
        func = getattr(xp, self.fname)
        a = testing.shaped_arange((10,), xp, dtype1)
        b = testing.shaped_arange((5,), xp, dtype2)
        with cupyx.allow_synchronize(False):
            return func(a, b)

    @testing.for_all_dtypes_combination(names=['dtype1', 'dtype2'])
    @testing.numpy_cupy_array_equal(accept_error=TypeError)
    def test_polyroutine_diff_types_poly1d(self, xp, dtype1, dtype2):
        func = getattr(xp, self.fname)
        a = testing.shaped_arange((10,), xp, dtype1)
        b = testing.shaped_arange((5,), xp, dtype2)
        a = xp.poly1d(a, variable='z')
        b = xp.poly1d(b, variable='y')
        with cupyx.allow_synchronize(False):
            out = func(a, b)
        assert out.variable == 'x'
        return out


@testing.gpu
class TestRoots(unittest.TestCase):

    @testing.for_signed_dtypes()
    @testing.numpy_cupy_allclose(rtol=1e-6)
    def test_roots1(self, xp, dtype):
        a = xp.array([2, -1, -2], dtype)
        out = xp.poly1d(a).roots
        return xp.sort(out)

    @testing.for_signed_dtypes()
    @testing.numpy_cupy_allclose(rtol=1e-6)
    def test_roots2(self, xp, dtype):
        a = xp.array([-4, 10, 4], dtype)
        out = xp.poly1d(a).roots
        return xp.sort(out)

    @testing.for_complex_dtypes()
    @testing.numpy_cupy_allclose(rtol=1e-6)
    def test_roots_complex(self, xp, dtype):
        a = xp.array([3j, 1.5j, -3j], dtype)
        out = xp.poly1d(a).roots
        return xp.sort(out)

    @testing.for_all_dtypes(no_float16=True, no_bool=True)
    @testing.numpy_cupy_array_equal()
    def test_roots_two_sized1(self, xp, dtype):
        a = xp.array([5, 10], dtype)
        return xp.roots(a)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal()
    def test_roots_two_sized2(self, xp, dtype):
        a = xp.array([0, 5], dtype)
        return xp.roots(a)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal()
    def test_roots_two_sized3(self, xp, dtype):
        a = xp.array([5, 0], dtype)
        return xp.roots(a)

    @testing.for_complex_dtypes()
    @testing.numpy_cupy_allclose(rtol=1e-6)
    def test_roots_two_sized_complex(self, xp, dtype):
        a = xp.array([3 + 2j, 5], dtype)
        return xp.roots(a)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal()
    def test_roots_one_sized(self, xp, dtype):
        a = xp.array([5], dtype)
        return xp.roots(a)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal()
    def test_roots_zero_sized(self, xp, dtype):
        a = xp.zeros((0,), dtype)
        return xp.roots(a)

    @testing.for_all_dtypes(no_bool=True)
    def test_roots_zero_dim(self, dtype):
        for xp in (numpy, cupy):
            a = testing.shaped_random((), xp, dtype)
            with pytest.raises(TypeError):
                xp.roots(a)

    @testing.for_all_dtypes(no_bool=True)
    def test_roots_ndim(self, dtype):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((3, 1), xp, dtype)
            with pytest.raises(ValueError):
                xp.roots(a)

    @testing.for_all_dtypes(no_bool=True)
    def test_roots_general(self, dtype):
        a = testing.shaped_arange((5,), cupy, dtype)
        with pytest.raises(NotImplementedError):
            cupy.roots(a)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal()
    def test_roots_zeros1(self, xp, dtype):
        a = xp.zeros((3,), dtype)
        return xp.roots(a)

    @testing.for_all_dtypes(no_bool=True)
    def test_roots_zeros2(self, dtype):
        for xp in (numpy, cupy):
            a = xp.zeros((2, 1), dtype)
            with pytest.raises(ValueError):
                cupy.roots(a)

    def test_roots_bool(self):
        a = testing.shaped_arange((5,), cupy, bool)
        with pytest.raises(NotImplementedError):
            cupy.roots(a)
