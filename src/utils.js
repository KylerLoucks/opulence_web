import { reactive, readonly} from "vue"


const state = reactive({
  isMobile: false,
})


const setMobile = (boolean) => {
  state.isMobile = boolean
}

export default {
  state: readonly(state),
  setMobile,
}