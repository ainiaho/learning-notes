### Link 
Markdown lnsert link 
<pre>
```markdown
  [text](url) 
```
</pre>
**example:**
[This is my blog](https://diepthink.top) 
### Insert photo
<pre>
  ```markdown
![Picture description,you can not write it](link of pictures)
  ```
</pre>
![My head portrait](https://avatars.githubusercontent.com/u/234639108?v=4&size=64)
### list 
#### Ordered list 
An ordered list uses numbers to add . sign plus a space to mark the list.
**example**
<pre>
  ```markdown
1. This is a ordered list
2. This is the second ordered list 
```
</pre>
**effect**
1. This is a ordered list 
2. This is the second ordered list 
#### Unordered list 
An unordered list uses * + - sign,and plus space to mark the list.
**example**
<pre>
  ```markdown
  * This is a unordered list
  + This is a unordered list
  - This is a unordered list
```
</pre>
  * This is a unordered list
  + This is a unordered list
  - This is a unordered list
Hierarchy
Use tap or plus space
**example**
<pre>
  ```markdown
 + unordered list 1
  +unordered list 2 
 1. ordered list
  2. ordered list
  ```
  </pre>
**effect**
+ unordered list 1 
  + unordered list 2 
1. ordered list
   1. ordered list
### Dividing line 
Use three - or * to build a dividing line 
<pre>
  ```markdown
  --- 
  ***
  ```
  </pre>
> --- 
  ***

### strikethrough 
Add two ~ sign
<pre>
  ```markdown
  ~~This is deleted text~~ 
  ```
  </pre>
~~This is deleted text ~~ 
### underline 
In text home and end ```<u>text</u>``` 
<u>The line has been undeerlined</u>
### code clock 
Markdown three are two types of code blocks Insert
First:In a line reference code can use <pre>` or ```
```</pre>
`The code`no code
```python (Decaration code type)
print("Hello world")
```
### Table 
"|"used to divide cells 
":-"align content left
"-:"align content right 
"-:-"align center content
effect
| Colmn1        | Column2        | Column3        |
| ------------- | -------------- | -------------- |
| Item1         | Item1          | Item1          |

### Footnote
<pre>[^]</pre> used to footnote
**effect**
Markdown can use footnote[^1]
special signs can be used \ indicated.
**effect**
<pre>\*  \+   ....</pre>
### Make a plan
```- [ ]```can indicates unfinished plan
```- [x]```can indicates finished plan
**effect**
- [ ] Study English
- [x] Study Markdown
### Write fornula
```$$```Represent an entire row formula
effect
$E=mc^2$
