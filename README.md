# Krita `localhost` Plugin

A tiny plugin that listens on localhost:12174 and allows you to issue arbitrary python commands to Krita.

<small>The port was chosen as it's the l33t spelling of "(K)RITA".</small>

Why?

* it allows you to control Krita from virtually any language (Bash, Golang, C++, you name it)
* you can play with Krita's API using your regular Linux editor `cat script.py | nc localhost 12174`.

## Usage

1. Import plugin into Krita (Tools -> Scripts -> Import Python Plugin from Web... -> `https://github.com/mafik/krita-localhost`). Alternatively download the zip file and use the `Import Python Plugin from File...` option.

2. In a terminal, use netcat to connect:

```sh
$> nc localhost 12174
print('hello world!')
hello world!
```

3. Profit!

## Limitations

Thread safety is based on having positive thoughts. It works for me but could cause some issues when you put it under load. If you know how to fix it, please do 🙏
