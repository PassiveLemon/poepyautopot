{ pkgs ? import <nixpkgs> { system = builtins.currentSystem; },
  lib ? pkgs.lib,
  python3Packages ? pkgs.python3Packages
}:

with python3Packages;

buildPythonApplication rec {
  pname = "poepyautopot";
  version = "1.2.3";

  src = ./.;

  nativeBuildInputs = [
    setuptools
  ];

  propagatedBuildInputs = [
    colorama
    evdev
    pillow
    pynput
    pyyaml
  ];
  
  doCheck = false;

  meta = with lib; {
    description = "A Python based Autopot script for Path of Exile";
    homepage = "https://github.com/passiveLemon/poepyautopot";
    changelog = "https://github.com/passiveLemon/poepyautopot/releases/tag/${version}";
    license = licenses.gpl3;
    maintainers = with maintainers; [ passivelemon ];
    platforms = [ "x86_64-linux" ];
  };
}
