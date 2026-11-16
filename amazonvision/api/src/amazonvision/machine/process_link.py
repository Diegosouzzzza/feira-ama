"""Link to a device that runs as a local process speaking the protocol on stdin/stdout.

Used to drive the real firmware logic compiled for the PC (firmware/test/native/harness.cpp)."""

import asyncio
import contextlib

from amazonvision.machine.link import LinkClosed


class ProcessLink:
    def __init__(self, command: list[str]) -> None:
        self._command = command
        self._process: asyncio.subprocess.Process | None = None

    async def start(self) -> None:
        self._process = await asyncio.create_subprocess_exec(
            *self._command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )

    def _alive(self) -> asyncio.subprocess.Process:
        process = self._process
        if process is None or process.returncode is not None:
            raise LinkClosed("processo do dispositivo encerrado")
        return process

    async def write(self, data: bytes) -> None:
        process = self._alive()
        assert process.stdin is not None
        try:
            process.stdin.write(data)
            await process.stdin.drain()
        except (BrokenPipeError, ConnectionResetError) as exc:
            raise LinkClosed(str(exc)) from exc

    async def read_line(self) -> bytes:
        process = self._alive()
        assert process.stdout is not None
        line = await process.stdout.readline()
        if not line:
            raise LinkClosed("fim da saída do dispositivo")
        return line

    async def control(self, instruction: str) -> None:
        """Test-only physical action on the simulated bench (e.g. 'estop 1', 'reboot')."""
        await self.write(f"#{instruction}\n".encode())

    async def close(self) -> None:
        process = self._process
        self._process = None
        if process is None or process.returncode is not None:
            return
        if process.stdin is not None:
            with contextlib.suppress(Exception):
                process.stdin.close()
        try:
            await asyncio.wait_for(process.wait(), timeout=2)
        except TimeoutError:
            process.kill()
            await process.wait()
