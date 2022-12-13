import { reactive, readonly} from "vue"


const state = reactive({
  isAuthenticated: false,
  skipAuthentication: false,
})


const setAuthenticated = (boolean) => {
  state.isAuthenticated = boolean
}

const skipAuth = (boolean) => {
  state.skipAuthentication = boolean
}

export default {
  state: readonly(state),
  setAuthenticated,
  skipAuth
}