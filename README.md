# dat220

## Database design

### Problem analysis
<mark style="background: #FF5582A6;">Entity</mark>, <mark style="background: #BBFABBA6;">attribute</mark>, <mark style="background: #ABF7F7A6;">relationship</mark>, 

The <mark style="background: #FF5582A6;">comments</mark> have a unique <mark style="background: #BBFABBA6;">comment id</mark>, a <mark style="background: #BBFABBA6;">user id</mark> which <mark style="background: #ABF7F7A6;">links</mark> to the <mark style="background: #FF5582A6;">user</mark>, a <mark style="background: #BBFABBA6;">post id</mark> that <mark style="background: #ABF7F7A6;">links</mark> to the <mark style="background: #FF5582A6;">post</mark> and <mark style="background: #BBFABBA6;">text</mark> displayed under the post.

The <mark style="background: #FF5582A6;">posts</mark> have a unique <mark style="background: #BBFABBA6;">post id</mark>, a <mark style="background: #ABF7F7A6;">reference</mark> to the <mark style="background: #BBFABBA6;">author</mark>, the <mark style="background: #BBFABBA6;">content</mark> and a <mark style="background: #BBFABBA6;">title</mark>.

The comments have a
