from audio import AudioPlayer


def test_player_has_aliases():
    player = AudioPlayer()
    assert hasattr(player, 'toggle_pause')
    assert hasattr(player, 'status')
