# weenix-script
A Python script to help add dbg() message

## HOW IT WORKS

If you want dbg() somewhere, you could left a special comment. This script will process all specified files, change these comments to formal commands with unique stamps. After we set many thest things, we could check weenix's output and find if these dbg print exist or not. If exists, we change former dbg() to standard dbg() we want.

## HOW TO USE
If you need a dbg() in example.c, simply type comment like

`/* NEED CHECK [: some words] */` 

Then, run `./check.py -p [filename]`

Next, `make clean` & `make`, run weenix and use `script` or `./weenix -n > record.txt` to save weenix's output. Remember to set DBG=print

Finally, run `./check.py -c [record] -f [c files] -t -t=[TAG NAME]`

## EXAMPLE
- In kernel/foo/exmaple.c, we have
```
if (ret) {
    do_some_work();
}
```
and we want to add a dbg().
- After adding a comment, example.c change to
```
if (ret) {
    /* NEED CHECK */
    do_some_work();
}
```

- Run `./check.py -p "kernel/*/*.c"`. File may change to
```
if (ret) {
    dbg(DBG_PRINT, "(DBG_HELPER O6OGF6G1DRFVZXB7U7TUAO0NM0G995VU_0)\n");
    do_some_work();
}
```
- `make clean; make`
- `./weenix -n > record.txt`
- Run a test in section X Y.Z
- `./check.py -c record.txt -f "kernel/*/*.c" -t "GRADINGX Y.Z"`
- If this code path is tested in section X Y.Z, example.c will change to
```
if (ret) {
    dbg(DBG_PRINT, "(GRADINGX Y.Z)\n");
    do_some_work();
}
```
