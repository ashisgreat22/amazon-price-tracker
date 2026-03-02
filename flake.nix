{
  description = "Amazon Price Tracker Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          requests
          beautifulsoup4
          lxml
          pytest
          requests-mock
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
          ];

          shellHook = ''
            echo "Amazon Price Tracker Dev Shell"
            echo "Python version: $(python --version)"
          '';
        };
      }
    );
}
