# save this as shell.nix
{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  packages = with pkgs; [
    python313
    python313Packages.pygame
    python313Packages.pyinstaller
  ];
}
