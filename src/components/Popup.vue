<!--
  Popup Component
  Displays Popups that are emitted to the event bus.

  Dependencies:
    - Requires the 'EventBus.js' mitt to pull popup events.
-->
<template>
    
    <div id="popup-container">
      <div v-for="popup in popups" :key="popup.id" class="popup-container">
        <transition name="popup" appear>
          <div class="popup" :style="{ borderColor: popup.borderColor }">
            <img
              class="icon"
              :alt="popup.icon"
              :src="iconPath(popup.icon)"
              draggable="false"
            />
            <div>{{ popup.message }}</div>
          </div>
        </transition>
      </div>
    </div>
    
  </template>
  
  <script>
  import emitter from '@/EventBus';
  
  export default {
    name: "PopupComponent",
    data() {
      return {
        popups: [],
      };
    },
    created() {
      emitter.on('showPopup', this.displayPopup);
    },
    beforeUnmount() {
      emitter.off('showPopup', this.displayPopup);
    },
    methods: {
      displayPopup(payload) {
        const message = payload.message
        const icon = payload.icon
        const borderColor = payload.borderColor
        const popup = {
            id: Date.now(), // Unique ID based on the current time
            message,
            icon,
            borderColor
        };
        this.popups.push(popup);
        
        setTimeout(() => {
            this.popups = this.popups.filter(p => p.id !== popup.id);
        }, 2500); // Hide popup after 2 seconds
      },

      iconPath(value) {
        return require(`@/assets/${value}.png`)
      },
    }
  };
  </script>
<style scoped>

#popup-container {
  position: fixed;
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  pointer-events: none;
}

.icon {
  width: 2em;
  height: 2em;
}

.popup-container {
  margin-top: 10px; /* Add vertical separation between popups */
}

.popup {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0,0,0,0.8);
  color: #fff;
  padding: .5em .5em;
  border-radius: .25em;
  border: 1px solid
}

/* Transition classes */
.popup-enter-active, .popup-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.popup-enter-from, .popup-leave-to {
  opacity: 0;
  transform: translate(0%, 100%);  /* Combined horizontal and vertical motion */
}
</style>

  