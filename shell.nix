{ pkgs ? import <nixpkgs> { } }:

pkgs.callPackage ./default.nix { }

# sudo ./result/bin/poepyautopot -f /home/lemon/.config/poepyautopot/config.yaml
