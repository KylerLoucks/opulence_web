import { reactive, readonly} from "vue"


const state = reactive({
  isAuthenticated: false
})


const setAuthenticated = (boolean) => {
  state.isAuthenticated = boolean
}

export default {
  state: readonly(state),
  setAuthenticated
}