title : Glide platformer : My first HTML5 game

date : 05-06-2014

description : Checkout the game I made in 24 hours using Phaser. Will you be able to beat the level 6 ? :)

author : volent

----------

### The game

I wanted to try Phaser for a while and found a free saturday, so I jumped on the occasion and made Glide. It's a platformer with 6 levels, the main character is a red guy moving his arms like an idiot and the goal is to reach the flag at the end of the level.

<script type="text/javascript" src="static/glide/phaser.min.js"></script>
<script type="text/javascript" src="static/glide/load.js"></script>
<script type="text/javascript" src="static/glide/menu.js"></script>
<script type="text/javascript" src="static/glide/end.js"></script>
<script type="text/javascript" src="static/glide/play.js"></script>
<script type="text/javascript" src="static/glide/main.js"></script>

<div id="game_div"></div>

### Tools I used

I found Phaser to be a really great library to get started with HTML5 gamedev. The [documentation](http://docs.phaser.io/) is well made, there is an [examples](http://examples.phaser.io/) for each functionnality and the [community](http://www.html5gamedevs.com/forum/14-phaser/) is awesome.

I used the [Tiled Map Editor](http://www.mapeditor.org/) to make the maps and I think it's the first time I had to read the doc of a software with GUI. Even if it took time to get used to it, it made the map creation process very fast.

### Things I've done

Glide is opensource and available on my Github : [https://github.com/volnt/Glide](https://github.com/volnt/Glide)

In order to include the game on the blog I had to use a little js "hack". The blog has a fixed width of 800px with 50px padding, but the game is 1000px width. In order for it to fit I just added `$('body').width(1100);` in the main.js file which inits the game.

I included the .tmx files (level/*.tmx) so you can edit any level I made using Tiled, so feel free to do a pull-request if you want me to add a new level. I will update the game on this page with your level.

### Conclusion

I hope you enjoyed the game and don't forget to leave a comment if you notice any bug :)

Tips for level 6 : You can crouch in the air & when you jump you go faster
