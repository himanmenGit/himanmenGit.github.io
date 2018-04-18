#Markdown

##Syntax guide

###Headers
```html
# This is an <h1> tag
## This is an <h2> tag
###### This is an <h6> tag
```

###Emphasis

	*This text will be italic*
	_This wiil also be italic_

	**This text will be bold**
	__This will also be bold__
	
	_You **can** combine them_
	
###List
####Unordered
	* item 1
	* item 2
		* item 2a
		* item 2b
			* item 2ba

####Ordered
	1. item 1
	2. item 2
	3. item 3
		1. item 3a
		2. item 3b
			1. item 3ba

###Images
	![images](https://octodex.github.com/images/yaktocat.png)

###Links
	http://github.com - automatic!1
	[GitGub](http://github.com)
	
###Blockquotes
	as Kanye West said:
	
	> We're living the future so
	> the present is out past
	
###Syntax highlignting
javascript
```javascript
function fancyAlert(arg){
	if(arg){
		$.facebox({div:'#foo'})
	}
}
```

or

	function fancyAlert(arg){
		if(arg){
			$.facebox({div:'#foo'})
		}
	}
	
python
```
def foo():
	if not bar:
		return True;
```

###Task Lists
```
- [x] @mentions, #refs, [links](), **formatting**, and <del>tags</del> supported
- [x] list syntax required (any unordered or ordered list supported)
- [x] this is a complete item
- [ ] this is an incomplete item
```

###Table
	First Header|Second Header
	------------|--------------
	Content from cell1 | Content from cell2
	Content in the first column | Content in the second column

###Strikethrough
	~~Strikethrough~~

###html
<input type=button value="input button"></input>









