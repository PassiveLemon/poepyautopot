{ pkgs ? import <nixpkgs> { system = builtins.currentSystem; },
  lib ? pkgs.lib,
  python3Packages ? pkgs.python3Packages
}:
python3Packages.buildPythonApplication rec {
  pname = "poepyautopot";
  version = "1.3.5";

  src = ./.;

  nativeBuildInputs = with python3Packages; [
    setuptools
  ];

  propagatedBuildInputs = with python3Packages; [
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
