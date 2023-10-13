import { socket } from './websocket'

import GameState from './GameState';


// rooms with socket io
export async function joinRoom(gameid) {
    return new Promise(( resolve, reject) => {
			try {
					console.log("Attempting to join game");
					socket.emit('join-room', { 'gameid': gameid }, (response) => {
									console.log("RESPONSE:", response);
									if (response.success) {
													console.log("SUCCESS RESPONSE!!");
											
													GameState.state.current_game_users = response.game_data.user_data
													GameState.state.current_game_card_shop = response.game_data.card_shop.cards
													GameState.state.current_turn_sid = response.current_turn_sid
													GameState.state.logs = response.logs
													GameState.state.sid = response.sid
													GameState.state.ingame = true
											
													
													// GameState.state.current_room_id = gameid;
											//     GameState.state.gameStarted = GameState.state.gamesList[gameid].started;
													resolve(true); // WebSocket join successful
									} else {
													console.log("RESPONSE WAS NOT SUCCESSFUL");
													reject(false); // WebSocket join failed
									}
					});
				} catch (error) {
								console.error('Error while joining room:', error);
								reject(false); // WebSocket join failed
				}
    })
}