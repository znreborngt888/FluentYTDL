from __future__ import annotations

from typing import Callable, Protocol


class POTManagerLike(Protocol):
    is_warm: bool

    def is_running(self) -> bool: ...

    def start_server(self) -> bool: ...

    def wait_until_ready(self, timeout: float = 15.0) -> bool: ...


def ensure_pot_provider_available(
    pot_manager: POTManagerLike,
    emit_log: Callable[[str], None],
    *,
    warm_timeout: float = 15.0,
) -> bool:
    """Start and warm POT provider when downloads need it."""

    if not pot_manager.is_running():
        emit_log("POT Provider 服务未运行，正在尝试启动...")
        if not pot_manager.start_server():
            emit_log("POT Provider 服务启动失败，本次下载将不使用 PO Token")
            return False

    if not pot_manager.is_warm:
        emit_log("POT Provider 正在初始化，请稍候...")
        pot_manager.wait_until_ready(timeout=warm_timeout)

    return pot_manager.is_running()
