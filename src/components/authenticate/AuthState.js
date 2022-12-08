import { reactive, readonly} from "vue"


const state = reactive({
  isAuthenticated: false,
  sub: null,
  userName: null
})


const setAuthenticated = (boolean) => {
  state.isAuthenticated = boolean
}

export default {
  state: readonly(state),
  setAuthenticated
}