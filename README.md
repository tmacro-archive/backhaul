
# Backhaul

**A game about the backhaul required to wage war on a intergalactic scale.**

> Like Dwarf Fortress but with more explosions! (explosions coming soon)

## Requirements
* Python 3.7 with sqlite support
* Possibly a C compiler for compiling PyPI dependencies

> Backhaul is tested and developed on Archlinux with a kernel version > 5.0.0. As the libraries used are portable Backhaul should run on other platforms, but they remain untested, and at this point in development **officially unsupported**

## Installation
> Currently backhaul has no packaging so the only option is to install using the source directly

**Clone the repo**
```
git clone https://github.com/tmacro/backhaul.git
cd backhaul
```
**Install the thing**
```
make install
```
## Regenerating Assests
All game tiles used in backhaul are generated using the tool `backhaul-assets` installed with the game.
Check the Makefile target `assets` for all tiles generated during install.
Custom colors can be used by modifying the Makefile or by running the `backhaul-assets`command by hand.

## Hacking on the code
A Makefile target is provided if you wish to install Backhaul in development mode.
Follow the installation instructions, substituting `make install` with `make develop`.


