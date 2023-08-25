from pathlib import Path
import shutil

from . import common as cm
import subprocess as sp
import os
import shlex


class SFMLBuilder(cm.Builder):
    def __init__(self, root_path: Path, deps: dict):
        super().__init__(root_path, deps, 'fmt')

    def prepare(self) -> cm.Result:
        # ==============================================================================================
        # sfml must be built
        # ==============================================================================================

        # ==============================================================================================
        # Create include directory and copy headers
        # ==============================================================================================
        if self.target_include_dir.exists():
            msg = f'[SFML]: \'{str(self.target_include_dir)}\' already exists'
            return cm.Result(cm.Error.FILE_EXISTS_WARNING, msg)
        else:
            self.target_include_dir.mkdir(parents=True)

        shutil.copytree(self.include_dir, self.target_include_dir)
        if not self.target_include_dir.exists():
            msg = f'[SFML]: failed to transact copy to \'{str(self.target_include_dir)}\''
            return cm.Result(cm.Error.FILE_COPY_FAILED, msg)

        # ==============================================================================================
        # Create build directory
        # ==============================================================================================
        if self.target_build_dir.exists():
            msg = f'[SFML]: \'{str(self.target_build_dir)}\' already exists'
            return cm.Result(cm.Error.FILE_EXISTS_WARNING, msg)
        else:
            self.target_build_dir.mkdir(parents=True)

        if not self.target_build_dir.exists():
            msg = f'[SFML]: failed to create directory \'{str(self.target_build_dir)}\''
            return cm.Result(cm.Error.FILE_MISSING, msg)

        return super().prepare()

    def build(self) -> cm.Result:
        # ==============================================================================================
        # Save current cwd
        # ==============================================================================================
        old_cwd: str = os.get_cwd()

        # ==============================================================================================
        # Build SFML in target build directory
        # ==============================================================================================
        cwd: Path = self.target_build_dir
        os.chdir(cwd)

        # ==============================================================================================
        # Run cmake to generate build configurations
        # ==============================================================================================
        cmd = shlex.split(
            f'cmake ../../../vendor/{self.name} -DCMAKE_BUILD_TYPE=Release')
        result: sp.CompletedProcess = sp.run(cmd)
        if result.returncode != 0:
            msg = f'[SFML]: cmake return code: {result.returncode}'
            msg += f'\nstdout: {result.stdout}'
            msg += f'\nstderr: {result.stderr}'
            return cm.Result(cm.Error.BUILD_TOOL_ERROR, msg)

        # ==============================================================================================
        # Use 'msbuild' to build it
        # FIXME: msbuild not used on any platform except windows
        # ==============================================================================================
        cmd = shlex.split(
            f'msbuild SFML.sln /t:CMake\\ALL_BUILD /p:Configuration="Release" /p:Platform="x64"')
        result: sp.CompletedProcess = sp.run(cmd)
        if result.returncode != 0:
            msg = f'[SFML]: msbuild return code: {result.returncode}'
            msg += f'\nstdout: {result.stdout}'
            msg += f'\nstderr: {result.stderr}'
            return cm.Result(cm.Error.BUILD_TOOL_ERROR, msg)

        # ==============================================================================================
        # Copy built library
        # ==============================================================================================
        lib_path: Path = self.target_build_dir / 'lib' / 'Release'
        if not lib_path.exists():
            msg = '[SFML]: path to compiler library directory not found'
            return cm.Result(cm.Error.FILE_MISSING, msg)

        sfml_audio_lib: Path = lib_path / 'sfml-audio-s.lib'
        sfml_graphics_lib: Path = lib_path / 'sfml-graphics-s.lib'
        sfml_main_lib: Path = lib_path / 'sfml-main-s.lib'
        sfml_network_lib: Path = lib_path / 'sfml-network-s.lib'
        sfml_system_lib: Path = lib_path / 'sfml-system-s.lib'
        sfml_window_lib: Path = lib_path / 'sfml-window-s.lib'

        lib_paths = [sfml_audio_lib, sfml_graphics_lib, sfml_main_lib,
                     sfml_network_lib, sfml_system_lib, sfml_window_lib]

        for lib in lib_paths:
            if not lib.exists():
                msg = '[SFML]: path to compiler library not found'
                return cm.Result(cm.Error.FILE_MISSING, msg)

            shutil.copy(lib, self.target_build_dir)

        # ==============================================================================================
        # Clean-up, restore old cwd
        # and remove all other directories and files associated with the build
        # ==============================================================================================
        os.chdir(old_cwd)

        for path in self.target_build_dir('**'):
            for lib in lib_paths:
                if path != lib and path.is_file():
                    path.unlink()
                elif path != lib and path.is_dir():
                    path.rmdir()

        return super().build()

    def clean(self) -> cm.Result:
        return super().clean()
