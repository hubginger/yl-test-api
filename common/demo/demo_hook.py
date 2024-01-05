"""
    跳过失败的用例
    逻辑是当前类中有一个失败了, 就跳过当前类

    最完美的实现是, 当前用例失败了, 凡是用到当前用例提取数据的用例, 都给跳过
    这个 .. emmm .. 有点难 ...
"""


from typing import Dict, Tuple
import pytest

# 全局变量，记录失败的用例
_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    # 判断用例执行失败后是否需要跳过
    if "incremental" in item.keywords:
        # 如果用例失败，添加到全局变量中
        if call.excinfo is not None:
            cls_name = str(item.cls)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            test_name = item.originalname or item.name
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    # 判断用例执行失败后是否需要跳过
    if "incremental" in item.keywords:
        cls_name = str(item.cls)
        # 判断当前用例的类是否在全局变量中
        if cls_name in _test_failed_incremental:
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # 如果当前类中的用例存在失败用例，就跳过
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))
