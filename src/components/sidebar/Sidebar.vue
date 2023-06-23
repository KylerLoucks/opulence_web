<template>
    <div class="sidebar" :style="{width: closed ? `10vw` : '30vw', marginTop: closed ? `0em` : `2.5em`, position: closed ? `relative` : `fixed`}"> 
        <span :id="closed ? 'collapse-icon' : 'rotate-180'" class="material-icons" @click="closed = !closed">chevron_right</span>
        <ChatLog class="chat-logs" :logs="logs"></ChatLog>

        <button class="leave-room-btn" v-on:click="$emit('leaveRoom', leaveRoom)">
            <span id="leave-icon" class="material-icons">logout</span>
            <span v-show="!closed" class="leave-txt">Leave</span>
        </button>
    </div>
    
</template>
  
  
<script>
    import {sidebarWidth} from './state';
    import ChatLog from "@/components/ChatLog.vue";
    
    
    export default {
    name: "SideBar",

    components: {
        ChatLog,
    },
    props: {logs: Array},
    setup() {
        return {
            sidebarWidth,
        };
    },
    data: function() {
        return {
            touch: {startX: 0, endX: 0 },
            closed: true,
        }
    },

    methods: {
        touchStart(event) {
            this.touch.startX = event.touches[0].clientX
            this.touch.endX = 0
        },
        touchEnd(event) {
            this.touch.endX = event.changedTouches[0].clientX
            console.log(Math.abs(this.touch.startX - this.touch.endX))
            if(Math.abs(this.touch.startX - this.touch.endX) < 20) return // distance to drag finger

            console.log(`start: ${this.touch.startX}`)
            console.log(`end: ${this.touch.endX}`)
            if (this.touch.endX < this.touch.startX) {
                this.closed = false;
            } 
            else {
                this.closed = true;
            }
            
        },

    },

    created: function() { // debugging the props
        // console.log(this.logs)

    },

    mounted: function() {

        // MOBILE TOUCH EVENTS
        this.$el.addEventListener('touchstart', event => {
            console.log(event)
            this.touchStart(event)
        })
        // this.$el.addEventListener('touchmove', event => {
        //     this.touchMove(event)
        // })
        this.$el.addEventListener('touchend', (event) => {
            this.touchEnd(event)
        })
        
    },

    computed: {
    },

    updated: function() {
    }
};
</script>
  
<style>
    :root{
        --sidebar-bg-color: linear-gradient(45deg, #726279, #5e30ff);
    }

</style>

<style scoped>

    .sidebar{
        color: white;
        background: var(--sidebar-bg-color);
        
        z-index: 1;
        
        top:0;
        bottom:0;
        right:0;
        

        transition: width 0.3s ease;

        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .sidebar #collapse-icon{
        transform: rotate(180deg);
        transition: 0.2s linear;
    }

    .chat-logs {
        background-color: #61636563;
        width: 100%;
        height: 65vh;

    }




    .leave-room-btn{
        position: absolute;
        bottom: 15px;
        height: 100%;
        width: 100%;
        max-width: 60%;
        max-height: 5vh;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: none;
        outline: none;
        border-radius: 5px;
        overflow: hidden; /* keep contents contained within */
        cursor: pointer; /* font size base for icon and text */
    }

    .leave-txt, #leave-icon{
        display: inline-flex;
        font-size: 100%;
    }



</style>