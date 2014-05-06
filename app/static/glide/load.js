var load_state = {
    preload: function() {
	game.stage.setBackgroundColor(0xffffff);

	text = this.game.add.text(250, 250, "loading..", {
	    font: '30px Arial',
	    fill: '#87E8D1'
	});

	this.game.load.image('scene', 'static/glide/assets/big_loading.png');
	this.game.load.image('loading', 'static/glide/assets/full_loading.png');
	this.game.load.image('flag', 'static/glide/assets/flag.png');
	this.game.load.spritesheet('character', 'static/glide/assets/character.png', 50, 50);
	this.game.load.image('top_stalactite', 'static/glide/assets/top_stalactite.png');
	this.game.load.image('bot_stalactite', 'static/glide/assets/bot_stalactite.png');
	this.game.load.image('background', 'static/glide/assets/background.png');
	this.game.load.spritesheet('jump_button', 'static/glide/assets/jump_button.png', 500, 250);
	this.game.load.spritesheet('crouch_button', 'static/glide/assets/crouch_button.png', 500, 250);
	this.game.load.spritesheet('run_button', 'static/glide/assets/run_button.png', 500, 500);

	this.game.load.tilemap('level1', 'static/glide/level/1.json', null, Phaser.Tilemap.TILED_JSON);
	this.game.load.tilemap('level2', 'static/glide/level/2.json', null, Phaser.Tilemap.TILED_JSON);
	this.game.load.tilemap('level3', 'static/glide/level/3.json', null, Phaser.Tilemap.TILED_JSON);
	this.game.load.tilemap('level4', 'static/glide/level/4.json', null, Phaser.Tilemap.TILED_JSON);
	this.game.load.tilemap('level5', 'static/glide/level/5.json', null, Phaser.Tilemap.TILED_JSON);
	this.game.load.tilemap('level6', 'static/glide/level/6.json', null, Phaser.Tilemap.TILED_JSON);
	this.game.load.image('map_tiles', 'static/glide/assets/tilemap.png');

    },

    create: function() {
	game.state.start('menu');
    },
};
