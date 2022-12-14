<template>
    <div v-if="!isLoaded" class="page-loader">
        <div class="half-circle-spinner">
            <div class="circle circle-1"></div>
            <div class="circle circle-2"></div>
        </div>
        <div class="loading-info-txt">{{loadingInfo}}</div>
    </div>
    
</template>
  
<script>
   
    export default {
    name: "PageLoader",

    props: {},
    setup() {
        return {
            
        };
    },
    data: function() {
        return {
            isLoaded: false,
            loadingInfo: ""
        }
    },

    methods: {

    },

    created: function() { // debugging the props
        // console.log(this.logs)

    },

    mounted() {
        this.loadingInfo = "Loading..."
        document.onreadystatechange = () => {
            if(document.readyState == "complete") {
                this.isLoaded = true
            }
        }
        
    },

    computed: {
    },

    updated: function() {
    }
};
</script>
  
<style>


</style>

<style scoped>

.page-loader {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: #333;
    z-index: 999;
}

.loading-info-txt {
    margin-top: 1em;
    color: white;
}

.half-circle-spinner, .half-circle-spinner * {
      box-sizing: border-box;
    }

    .half-circle-spinner {
      width: 5rem;
      height: 5rem;
      border-radius: 100%;
      position: relative;
    }

    .half-circle-spinner .circle {
      content: "";
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 100%;
      border: calc(60px / 10) solid transparent;
    }

    .half-circle-spinner .circle.circle-1 {
      border-top-color: #ff1d5e;
      animation: half-circle-spinner-animation 1s infinite;
    }

    .half-circle-spinner .circle.circle-2 {
      border-bottom-color: #ff1d5e;
      animation: half-circle-spinner-animation 1s infinite alternate;
    }

    @keyframes half-circle-spinner-animation {
      0% {
        transform: rotate(0deg);

      }
      100%{
        transform: rotate(360deg);
      }
    }

</style>