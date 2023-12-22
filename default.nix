{ pkgs ? import <nixpkgs> { system = builtins.currentSystem; },
  lib ? pkgs.lib,
  python3Packages ? pkgs.python3Packages
}:

with python3Packages;

buildPythonApplication rec {
  pname = "poepyautopot";
  version = "1.2.2";

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

  # There is currently an issue where config.yaml is not included along side the other files. This results in a failure to write the config file to the users config directory.
  # This phase should manually add it but 'python3.XX' is not always the same so it's not super effective.
  #installPhase = ''
    #mkdir -p $out/lib/python3.11/site-packages/poepyautopot/
    #cp $src/poepyautopot/config.yaml $out/lib/python3.11/site-packages/poepyautopot/config.yaml
  #'';
  
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
