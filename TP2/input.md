# Markdown Test File

## Header2

### Header3

#### Header4

##### Header5

###### Header6

## Text Formatting

This is a **bold** text with more __bold__ text.

This is an *italic* text with more _italic_ text.

This is a ***bold and italic*** text with more ___bold and italic___ text.

This is a ~~strikethrough~~ text.

<u>This is an underline text that shoudn't be touched at all</u>

Some text with `inline code` and without paragraphs
directly in the same line. \
This is a new line but not a new paragraph \
This is another new line but not a new paragraph
and this should appear in the same line as the previous one.

This is a new paragraph.

multiple   spaces    between    words

## Blockquotes

> This is a blockquote.

Random > paragraph.

>>> Pretty funny >>> blockquote.

> Multiple lines \
> of blockquote
>>
>>> with nested blockquote
> in the middle
>>
>> decreasing level
>> test
> 
>> another test
>>
> the end

> Roller
>>> Coaster
>
> Yay

> a
>

>

> testing this
blockquote \
hehehehe

## Lists

### Ordered List

1. First item
2. Second item
3. Third item
    1. Subitem 1
    2. Subitem 2

### Unordered List

- Item 1
- Item 2
  - Subitem 1
  - Subitem 2

## Code

Inline code: `print("Hello, world!")` \
Weird inline code format: The spaces are` inside the backticks `XD

Code block:

```
code block without language
```

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Crazy")
```

```elixir
IO.puts "This is another block of code"
```

Why not put some example from `stackoverflow` without a paragraph? \
This is the `Panel` constructor:

```javascript
function Panel(element, canClose, closeHandler) {
  this.element = element;
  this.canClose = canClose;
  this.closeHandler = function () { if (closeHandler) closeHandler() };
}
```

## Horizontal Rule

---

---------------

A --- B

## Links and Images

[This is a link to Google](https://www.google.com)

![Alt text](https://picsum.photos/200/300)

[]()

![]()

## Tricky situations

##Almost a header

##

Random ### not a header

`---`

--- shoudn't be a horizontal rule

`## header`

-not a list

* foo
*   
* bar

+

foo
1.

1.
2.
   3.
      4.

+ foo
 + bar
  + baz
   + boo

1-
2-
3.

1.hvhv

1.    foo

   - 1

1. hello
2. there
    1. hahaha
    2. hehehe

list separator

1. hello
2. there
    - hahaha
    - hehehe

`` foo ` bar  ``

``
foo
``

`foo   bar
  baz`

line break  
test

**Bold** text next to each other without space**bold again**

*Italic* text next to each other without space*italic again*

Some *italic **intercalated with** bold* text and some **bold *intercalated with* italic** text

\*\*This is not bold\*\* and ***this is bold**

**This should be bold***

**Bold * asterisk**

\*This is not italic\* and **this is italic*

*This should be italic**

\~\~This is not strikethrough\~\~ and ~~~this is strikethrough~~

~~This should be strikethrough~~~

\<u\>This is not underline, it's escaped HTML\</u\>

*this is italic
in multiple* *lines of text
dwadwd dwadwa*


a> ball > jumping>high

  test>>GT><<LTconversion< <without spaces
