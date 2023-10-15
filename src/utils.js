import { reactive, readonly} from "vue"


const state = reactive({
  isMobile: false,
  createdGame: false,
  joinSuccessful: false
})


const setMobile = (boolean) => {
  state.isMobile = boolean
}

const setCreatedGame = (boolean) => {
  state.createdGame = boolean
}

const setJoinSuccessful = (boolean) => {
  state.joinSuccessful = boolean
}

export default {
  state: readonly(state),
  setMobile,
  setCreatedGame,
  setJoinSuccessful
}