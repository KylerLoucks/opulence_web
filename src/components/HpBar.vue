<template>

    <div class="container">
        <div :style="fillerStyles">
            <span class="label">{{ `${value}` }}</span>
        </div>
    </div>
</template>
  
  
<script>
    import { computed } from "vue";
    
    export default {
    name: "ProgressBar",
   
    props: { // variables when instantiating this component
        bgcolor: String,
        value: Number,
        vines: Number,
    },
    setup() {
        // const fillerStyles = computed(() => {
        //     return {
        //         height: "100%",
        //         width: `${props.value * 10}%`,
        //         backgroundColor: props.bgcolor,
        //         transition: "width 1s ease-in-out",
        //         borderRadius: "inherit",
        //         textAlign: "right",
        //     };
        // });
        // return { fillerStyles };
    },

    data(props) {
        var fillerStyles = computed(() => {
            var color = this.getBarColor()
            return {
                height: "100%",
                width: `${props.value * 10}%`,
                maxWidth: "25em",
                backgroundColor: color,
                transition: "width 1s ease-in-out",
                borderRadius: "inherit",
                textAlign: "right",
            };
        });
        return { fillerStyles };
    },

    methods: {
        getBarColor() {
            if (this.vines > 0) {
                return "#25854f"
            } else {
                return this.bgcolor
            }
            
        }
    },


    created: function() { // debugging the props
    },

    updated: function() {
    }
};
</script>
  
<style scoped>
    .container {
    height: 15px;
    max-height: 5.2vw;
    width: 100%;
    max-width: 16em;
    background-color: #e0e0de34;
    border-radius: 50px;
    
    /* margin: 15px;
    margin-left: auto;
    margin-right: auto; */
    
    }

    .label {
    padding: .3em;
    margin: .2em;
    color: white;
    font-weight: bold;
    }
</style>