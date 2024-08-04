# Krita `localhost` Plugin

A tiny plugin that listens on localhost:12174 and allows you to issue arbitrary python commands to Krita.

<small>The port was chosen as it's the l33t spelling of "(K)RITA".</small>

## Usage

1. Import plugin into Krita (Tools -> Scripts -> Import Python Plugin from Web... -> `https://github.com/mafik/krita-localhost`).

2. In a terminal, use netcat to connect:

```sh
$> nc localhost 12174
print('hello world!')
hello world!
```

3. Profit!
