{ pkgs ? import <nixpkgs> { } }:

pkgs.callPackage ./default.nix { }

# sudo LD_LIBRARY_PATH=$LD_LIBRARY_PATH PYTHONPATH=$PYTHONPATH python3 poepyautopot/__main__.py -f ~/.config/poepyautopot/config.yaml
