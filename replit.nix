{ pkgs }: {
    deps = [
        pkgs.python39
        pkgs.python39Packages.pip
        pkgs.portaudio
        pkgs.ffmpeg
        pkgs.nodejs
        pkgs.nodePackages.typescript
        pkgs.libuuid
        pkgs.openssl
        pkgs.git
    ];
    env = {
        PYTHONBIN = "${pkgs.python39}/bin/python3.9";
        LANG = "en_US.UTF-8";
    };
} 