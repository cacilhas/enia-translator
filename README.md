# EN-IA Translator

This application searches on-line for English words and returns their
[Interlingua](http://www.interlingua.com/) matching.

It requires [Python 3.6+](https://www.python.org/) and use some dependences:

- [`appdirs` 1.4.3](https://github.com/ActiveState/appdirs)
- [`lxml` 4.2.1](http://lxml.de/)
- [`requests` 2.18.4](http://docs.python-requests.org/en/master/)

## Use

Just call `en-ia` followed by the word to be searched:

```
$ en-ia ALL
ALL adj omne, tote; adv completemente; (everybody) omnes, totes; (everything)
    toto; (at - ) del toto
```

## Wordbook

The source for matches is the
[Union Mundial pro Interlingua](http://www.interlingua.com/an/ceid).

## TODO

- Support other languages without configfile edition.
- Support inexact search.

## Copyrights

It’s under the [3-Clause BSD License](https://opensource.org/licenses/BSD-3-Clause).

You can read the copying text
[here](https://bitbucket.org/cacilhas/enia-translator/src/master/COPYING).
