# Gaia

A work-in-progress golfing language inspired by [CJam](https://sourceforge.net/projects/cjam/), [Jelly](https://github.com/DennisMitchell/jelly), [Ohm](https://github.com/nickbclifford/Ohm), and [SOGL](https://github.com/dzaima/SOGL).

Gaia is still very much incomplete. Currently it's more or less usable but still has a very limited set of operators and built-in functions.

Documentation is currently unavailable, because I haven't even designed the entire spec yet.

## Running Gaia

Download the four `.py` files, and run `python gaia.py <flags, optionally> <filename>`.

Currently the only flag supported is `-e`, to run using the codepage encoding.

## Basic Syntax

Gaia is stack-based, so all operators and functions are written in postfix notation. There are three data types in Gaia: number, string, list. All operators do something different for each data type. For example, the operator `$`

 - converts a number to a list of digits;
 - converts a string to a list of characters; or
 - joins a list into a string, with no separator.
 
Not every operator supports all types or combinations of types.
