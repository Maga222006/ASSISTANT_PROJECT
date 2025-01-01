{ pkgs }: {
    deps = [
        pkgs.python310
        pkgs.python310Packages.pip
        pkgs.portaudio
        pkgs.ffmpeg
        pkgs.gcc
        pkgs.python310Packages.wheel
        pkgs.python310Packages.setuptools
    ];
} 