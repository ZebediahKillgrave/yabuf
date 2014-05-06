var game = new Phaser.Game(1000, 500, Phaser.AUTO, 'game_div');
$('body').width(1100); // little hack so it fits in the blog

game.state.add('load', load_state);
game.state.add('menu', menu_state);
game.state.add('play', play_state);
game.state.add('end', end_state);

game.state.start('load');
