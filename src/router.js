// In your router.js or router configuration file
import { createRouter, createWebHistory } from 'vue-router'
import AuthState from "./components/authenticate/AuthState"
import { userPool } from './components/authenticate/UserPool'

// import { joinRoom } from './joinhelper'

import utils from './utils'

const routes = [
  {
    path: '/',
    redirect: () => {
			if (userPool.getCurrentUser()) {
				return '/home';
			} else {
				return '/login';
			}
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('./views/Login.vue'),
		beforeEnter: (to, from, next) => {
			if (userPool.getCurrentUser()) {
				next('/home')
			} else {
				next();
			}
		}
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('./views/Home.vue'),
    beforeEnter: (to, from, next) => {
      // Check if the user is authenticated
      if (userPool.getCurrentUser() || AuthState.state.skipAuthentication) {
        // User is authenticated, allow access to the route
        next();
      } else {
        // User is not authenticated, redirect to the login page
        next('/login');
      }
    }
  },
  {
		path: '/game/:gameid', // Dynamic route with a parameter
		name: 'game',
		component: () => import('./views/Game.vue'),
		props: false, // Pass route params as props to the component
		beforeEnter: (to, from, next) => {
			try {
			const gameId = to.params.gameid;
			const createdGame = utils.state.createdGame
			console.log(gameId)
			console.log("route param creategame: ", createdGame)

			if (createdGame) {
				utils.setCreatedGame(false)
				// Route navigation can proceed
				next();
			} else if (utils.state.joinSuccessful) {
				utils.setJoinSuccessful(false)
				next();
			} else {
				next('/error')
			}
		} catch (err) {
			console.log("ERROR with router: " + err)
		}


			// } else {
			// 	await joinRoom(gameId)
			// 	.then(() => {
			// 		// Route navigation can proceed
			// 		next();
			// 	})
			// 	.catch((error) => {
			// 		console.log("error joining game: ", error)
			// 		// Handle the error or redirect as needed
			// 		next('/error');
			// 	});
			}
	},
  // ...other routes
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
