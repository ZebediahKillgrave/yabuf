title : Highlight your code with markdown, codehilite and pygments

date : 04-07-2014

----------

In this post I will explain how I highlight the code blocks on the blog. I think it's the easiest way to do it and probably the way most people do it.

The goal is to generate HTML code from Markdown and then highlight the code.

You will need two python modules that you can install using pip :

>     pip install pygments
>     pip install markdown

We will also use a markdown plugin called codehilite but there's nothing to download, it comes with markdown.

Now, let's put nice colors on some python code :

    :::python   
    >>> from markdown import markdown
    >>> markdown("""
    ...    :::python
    ...    def printf(msg="Hello World !"):
    ...	       '''Wrap print statement in a function'''
    ...        print msg
    ...""", ['codehilite'])
    u'<div class="codehilite"><pre><span class="k">def</span> <span class="nf">printf</span><span class="p">(</span><span class="n">msg</span><span class="o">=</span><span class="s">&quot;Hello World !&quot;</span><span class="p">):</span>\n    <span class="sd">&#39;&#39;&#39;Wrap print statement in a function&#39;&#39;&#39;</span>\n    <span class="k">print</span> <span class="n">msg</span>\n</pre></div>'

So we got some HTML with many `<span>` blocks but if you try to display that, it won't be highligted. This is were we need pygments, it will generate a css file that will highlight the code based on the class specified by codehilite.

    pygmentize -f html -S default -a .codehilite > highlight.css

Now you just have to use that css in your html file and you're all set !

See the example highlighted :

    :::python
    def printf(msg="Hello World !"):
    	'''Wrap print statement in a function'''
        print msg

Hope you liked that quick post !
