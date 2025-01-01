{ pkgs }: {
    deps = [
        pkgs.python310
        pkgs.python310Packages.pip
        pkgs.portaudio
        pkgs.ffmpeg
        pkgs.gcc
        pkgs.gcc-unwrapped
        pkgs.gcc-unwrapped.lib
        pkgs.cmake
        pkgs.gnumake
        pkgs.pkg-config
        pkgs.python310Packages.wheel
        pkgs.python310Packages.setuptools
        pkgs.alsa-lib
        pkgs.libpulseaudio
        pkgs.swig
    ];
    env = {
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.gcc-unwrapped.lib
            pkgs.alsa-lib
            pkgs.libpulseaudio
        ];
    };
} 