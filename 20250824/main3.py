from fastapi import Depends


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)
"""
これは依存関係とyieldの例
1. dependency_a が呼ばれる

dep_a = generate_dep_a() が実行される

yield dep_a に到達して一時停止

2. dependency_b が呼ばれる（dep_a を引数に受け取る）

dep_b = generate_dep_b() が実行される

yield dep_b に到達して一時停止

3. dependency_c が呼ばれる（dep_b を引数に受け取る）

dep_c = generate_dep_c() が実行される

yield dep_c に到達して一時停止

これで依存関係が解決し、エンドポイントにdep_cが渡される

クリーンアップ

1. dependency_c の finally

dep_c.close(dep_b)


2. dependency_b の finally

dep_b.close(dep_a)


3. dependency_a の finally

dep_a.close()

これでリソースが安全に解放される
"""