# static analysis: ignore
from .value import TypedValue
from .implementation import assert_is_value
from .test_node_visitor import assert_passes
from .test_name_check_visitor import TestNameCheckVisitorBase


class TestNoReturn(TestNameCheckVisitorBase):
    @assert_passes()
    def test_no_return(self):
        from typing_extensions import NoReturn
        from typing import Optional

        def f() -> NoReturn:
            raise Exception

        def capybara(x: Optional[int]) -> None:
            if x is None:
                f()
            assert_is_value(x, TypedValue(int))

    @assert_passes()
    def test_no_return_parameter(self):
        from typing_extensions import NoReturn

        def assert_unreachable(x: NoReturn) -> None:
            pass

        def capybara():
            assert_unreachable(1)  # E: incompatible_argument

    @assert_passes()
    def test_assignability(self):
        from typing_extensions import NoReturn

        def takes_never(x: NoReturn):
            print(x)


class TestAssertNever(TestNameCheckVisitorBase):
    @assert_passes()
    def test_if(self):
        from pyanalyze.tests import assert_never
        from typing import Union

        def capybara(x: Union[int, str]) -> None:
            if isinstance(x, int):
                print("int")
            elif isinstance(x, str):
                print("str")
            else:
                assert_never(x)


class TestNeverCall(TestNameCheckVisitorBase):
    @assert_passes()
    def test_empty_list(self):
        def callee(a: int):
            pass

        def capybara():
            for args in []:
                callee(*args)

            for kwargs in []:
                callee(**kwargs)
