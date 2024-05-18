{ pkgs }: {
    deps = [
      pkgs.heroku
      pkgs.podman
        pkgs.python39
        pkgs.python39Packages.pip
        pkgs.python39Packages.virtualenv
    ];
}
