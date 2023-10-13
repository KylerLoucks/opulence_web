import { reactive, readonly} from "vue"


const state = reactive({
  isMobile: false,
  createdGame: false,
})


const setMobile = (boolean) => {
  state.isMobile = boolean
}

const setCreatedGame = (boolean) => {
  state.createdGame = boolean
}

export default {
  state: readonly(state),
  setMobile,
  setCreatedGame
}