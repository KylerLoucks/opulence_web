import { ref, computed } from 'vue'
export const collapsed = ref(false)

// set the sidebar boolean to the opposite (e.g true = false, false = true)
export const toggleSidebar = () => {
    collapsed.value = !collapsed.value
}

export const SIDEBAR_WIDTH = 35
export const SIDEBAR_WIDTH_COLLAPSED = 25
export const sidebarWidth = computed( () => 
    `${collapsed.value ? SIDEBAR_WIDTH_COLLAPSED : SIDEBAR_WIDTH}vw`
)


