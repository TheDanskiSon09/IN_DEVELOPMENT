"""The module contains the implementation of base audio class"""

from platform import system
from threading import Thread, Event
from NarratorEngine.entity import Entity
from NarratorEngine.exceptions import AudioFileNotFoundError

if system() == 'Windows':
    from winsound import PlaySound, SND_FILENAME, SND_ASYNC, SND_LOOP, SND_PURGE


class Audio(Entity):

    def __init__(
        self,
        filepath: str
    ) -> None:
        from os.path import exists
        if not exists(filepath):
            raise AudioFileNotFoundError(f"No such file or directory: '{filepath}'")
        self.filepath = filepath
        self.system = system()
        self._thread = None
        self._process = None
        self._stop_event = Event()
        self._repeat = 1
        self.create_entity()

    def play(
            self,
            repeat: int = 1
    ) -> None:
        self.stop()
        self._repeat = repeat
        self._stop_event.clear()
        self._thread = Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self):
        from contextlib import suppress
        self._stop_event.set()
        if self.system == 'Windows':
            with suppress(Exception):
                PlaySound(None, SND_PURGE)
        else:
            if self._process:
                with suppress(Exception):
                    self._process.terminate()
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=0.2)

    def _worker(self):
        if not self.game.is_android() and self.game.enable_audio:
            if self.system == 'Windows':
                self._play_windows()
            elif self.system == 'Darwin':
                self._play_unix(['afplay'])
            else:
                player = self._detect_linux_player()
                if not player:
                    print('[Audio] No suitable audio player found.')
                    return
                self._play_unix(player)

    def _play_windows(self):
        flags = SND_FILENAME | SND_ASYNC
        if self._repeat == -1:
            PlaySound(self.filepath, flags | SND_LOOP)
            self._stop_event.wait()
        else:
            for _ in range(self._repeat):
                if self._stop_event.is_set():
                    break
                PlaySound(self.filepath, flags)
                self._wait_windows_duration()

    def _play_unix(
            self,
            command: str
    ) -> None:
        from subprocess import Popen
        if self._repeat == -1:
            while not self._stop_event.is_set():
                self._process = Popen(command + [self.filepath])
                self._process.wait()
        else:
            for _ in range(self._repeat):
                if self._stop_event.is_set():
                    break
                self._process = Popen(command + [self.filepath])
                self._process.wait()

    def _detect_linux_player(self):
        from shutil import which
        for cmd in [['paplay'], ['aplay'], ['ffplay', '-nodisp', '-autoexit']]:
            if which(cmd[0]):
                return cmd
            return None

    def _wait_windows_duration(self):
        from time import sleep
        try:
            from wave import open
            with open(self.filepath, 'rb') as soundfile:
                duration = soundfile.getnframes() / soundfile.getframerate()
                sleep(duration)
        except Exception:
            sleep(1)
