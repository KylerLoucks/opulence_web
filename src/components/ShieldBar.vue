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
    name: "ShieldProgressBar",
   
    props: { // variables when instantiating this component
        bgcolor: String,
        value: Number,
        shieldType: String,
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
            if (this.shieldType == 'FIRE')return "#dd221e"
            else if (this.shieldType == 'WATER')return "#3f7ab6" 
            else if (this.shieldType == 'DARK')return "#200f34" 
            else if (this.shieldType == 'ARCANE')return "#7332b7" 
            else if (this.shieldType == 'EARTH')return "#865b38" 
            else if (this.shieldType == 'NATURE')return "#5ec234" 
            else if (this.shieldType == 'SOLAR')return "#c9721f" 
            else if (this.shieldType == 'WIND')return "#b7b7b7" 
            else return this.bgcolor
            
        }
    },


    created: function() { // debugging the props
        
    },

    mounted: function() {
    },

    updated: function() {
    }
};
</script>
  
<style scoped>
    .container {
    height: 15px;
    max-height: 1.2vw;
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