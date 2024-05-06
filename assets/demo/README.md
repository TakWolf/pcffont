# Demo Fonts

- [bdftopcf](https://gitlab.freedesktop.org/xorg/util/bdftopcf)
- [bdftopcf - docs](https://www.x.org/releases/current/doc/man/man1/bdftopcf.1.xhtml)

```shell
bdftopcf demo.bdf -o demo-lsbyte-lsbit-p4-u2.pcf -L -l -p4 -u2
bdftopcf demo.bdf -o demo-lsbyte-msbit-p4-u2.pcf -L -p4 -u2
bdftopcf demo.bdf -o demo-msbyte-lsbit-p4-u2.pcf -l -p4 -u2
bdftopcf demo.bdf -o demo-msbyte-msbit-p4-u2.pcf -p4 -u2

bdftopcf demo.bdf -o demo-lsbyte-lsbit-p2-u4.pcf -L -l -p2 -u4
bdftopcf demo.bdf -o demo-lsbyte-msbit-p2-u4.pcf -L -p2 -u4
bdftopcf demo.bdf -o demo-msbyte-lsbit-p2-u4.pcf -l -p2 -u4
bdftopcf demo.bdf -o demo-msbyte-msbit-p2-u4.pcf -p2 -u4

bdftopcf demo.bdf -o demo.pcf
bdftopcf demo-2.bdf -o demo-2.pcf
```
