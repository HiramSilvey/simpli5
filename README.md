# simpli5
simpli5 is an API that automatically create simplified version of texts that is easier to understand.
It auto-detect part of the sentence and replaces uncommon words with simpler phrases in text.

To use simpli5, call simpli5(paragraph) with a paragraph of text to be simlified. 

## Motivation ##
Ever gone to a Wikipedia page of something you were intested in, started to read it, and quickly realized the material was way over your head? (I find this happens most frequently on math-related pages for me!) Fortunately, many Wikipedia pages are available in many language translations - one of which may be 'Simple English.' The 'Simple English' language on Wikipedia restricts the pages to using only the most common English words, so that that may become easier to parse for non-experts. Although there's a lot to gain from creative analogies of problems, perhaps a simple word swap could also improve the readability of complicated texts as well. This approach is much easier to start with, and could provide the first step to automating this simplification of English.

## Installation ##

OSX:

Install `pip` if you don't have it already.

run `pip install requirements.txt`

add `import simpli5.parser` to python files you want to use simpli5 in

call `simple_text = simpli5.parser.simpli5('some complicated text here!')` to get the 'simpli5'd version'
