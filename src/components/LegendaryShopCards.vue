<template>   
<div class="parent-container">
    <button ref="cardButton"  class="card-button" v-on:click="$emit('buyCard', buyCard)">
        <div class="damage-type-image-stats">
            <span class="tooltip-cardshop" data-hover="Attack Card" v-if="spellType == 'ATTACK'"><img draggable="false" src="@/assets/sword.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span>
            <span class="tooltip-cardshop" data-hover="Defence Card" v-else-if="spellType == 'SHIELD'" ><img draggable="false" src="@/assets/shield.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span> 
            <span class="tooltip-cardshop" data-hover="Mundane" v-else> <img draggable="false" src="@/assets/mundane.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span>
            <h3 class="damage-value">{{power}}</h3>
        </div>


        <h3 class="idvalue">Purchase</h3>
        <div class="affinity-stats">
            <span v-if="runeType == 'WIND'" class="tooltip-cardshop" data-hover="Wind Afinity" ><img draggable="false" src="@/assets/WIND.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span>
            <span v-else-if="runeType == 'FIRE'" class="tooltip-cardshop" data-hover="Fire Affinity" ><img draggable="false" src="@/assets/FIRE.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;" /></span>
            <span v-else-if="runeType == 'WATER'" class="tooltip-cardshop" data-hover="Water Affinity" ><img draggable="false" src="@/assets/WATER.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span>
            <span v-else-if="runeType == 'SOLAR'" class="tooltip-cardshop" data-hover="Solar Affinity" ><img draggable="false" src="@/assets/SOLAR.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span>
            <span v-else-if="runeType == 'DARK'" class="tooltip-cardshop" data-hover="Dark Affinity" ><img draggable="false" src="@/assets/DARK.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span>
            <span v-else-if="runeType == 'ARCANE'" class="tooltip-cardshop" data-hover="Arcane Affinity" ><img draggable="false" src="@/assets/ARCANE.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span>
            <span v-else-if="runeType == 'EARTH'" class="tooltip-cardshop" data-hover="Earth Affinity"  ><img draggable="false" src="@/assets/EARTH.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span>
            <span v-else-if="runeType == 'NATURE'" class="tooltip-cardshop" data-hover="Nature Affinity" ><img draggable="false" src="@/assets/NATURE.png" style="width:100%; max-width: 2em; max-height: 2em; height: 100%;"/></span>
            <h3 class="affinity-value">{{affinity}}</h3>
        </div>
    </button>


    
    <div class="cost-container">
        <div v-if="cost.SOLAR" class="icon-text-container">
            <h3 ref="solarCost" class="text">x{{cost.SOLAR}}</h3>
            <img class="cost-icons" draggable="false" src="@/assets/SOLAR.png"/>
        </div>
        <div v-if="cost.WATER" class="icon-text-container">
            <h3 ref="waterCost" class="text">x{{cost.WATER}}</h3>
            <img class="cost-icons" draggable="false" src="@/assets/WATER.png"/>
        </div>
        <div v-if="cost.ARCANE" class="icon-text-container">
            <h3 ref="arcaneCost" class="text">x{{cost.ARCANE}}</h3>
            <img class="cost-icons" draggable="false" src="@/assets/ARCANE.png"/>
        </div>
        <div v-if="cost.WIND" class="icon-text-container">
            <h3 ref="windCost" class="text">x{{cost.WIND}}</h3>
            <img class="cost-icons" draggable="false" src="@/assets/WIND.png"/>
        </div>
        <div v-if="cost.FIRE" class="icon-text-container">
            <h3 ref="fireCost" class="text">x{{cost.FIRE}}</h3>
            <img class="cost-icons" draggable="false" src="@/assets/FIRE.png"/>
        </div>
        <div v-if="cost.NATURE" class="icon-text-container">
            <h3 ref="natureCost" class="text">x{{cost.NATURE}}</h3>
            <img class="cost-icons" draggable="false" src="@/assets/NATURE.png"/>
        </div>
        <div v-if="cost.DARK" class="icon-text-container">
            <h3 ref="darkCost" class="text">x{{cost.DARK}}</h3>
            <img class="cost-icons" draggable="false" src="@/assets/DARK.png"/>
        </div>
        <div v-if="cost.EARTH" class="icon-text-container">
            <h3 ref="earthCost" class="text">x{{cost.EARTH}}</h3>
            <img class="cost-icons" draggable="false" src="@/assets/EARTH.png"/>
        </div>
    </div>
</div> 

</template>
  
  
<script>
    import utils from '@/utils';

    export default {
    name: "CardsInShop",
   
    props: { // variables when instantiating this component
        cost: Object,
        affinity: Number,
        power: Number,
        runeType: String,
        spellType: String,
        users: Array,
        currentTurnSid: String,
    },
    setup() {
        return {
        };
    },

    data: function() {
        return {
            utils
        }
    },

    methods: {
        updateCardBtnBackground: function() {
            var element = this.$refs.cardButton;
            element.style.backgroundRepeat = "no-repeat"


            element.style.backgroundSize = "100% 150px"

            if (utils.state.isMobile) {
                element.style.backgroundSize = "100% 250px"
            }

            switch(this.runeType) {
                case "ARCANE":
                    element.style.backgroundImage = 'url(' + require('@/assets/arcane_card.png') + ')'
                    break;
                case "WIND":
                    element.style.backgroundImage = 'url(' + require('@/assets/wind_card.png') + ')'
                    break;
                case "EARTH":
                    element.style.backgroundImage = 'url(' + require('@/assets/earth_card.png') + ')'
                    break;
                case "FIRE":
                    element.style.backgroundImage = 'url(' + require('@/assets/fire_card.png') + ')'
                    break;
                case "SOLAR":
                    element.style.backgroundImage = 'url(' + require('@/assets/solar_card.png') + ')'
                    break;
                case "NATURE":
                    element.style.backgroundImage = 'url(' + require('@/assets/nature_card.png') + ')'
                    break;
                case "DARK":
                    element.style.backgroundImage = 'url(' + require('@/assets/dark_card.png') + ')'
                    break;
                case "WATER":
                    element.style.backgroundImage = 'url(' + require('@/assets/water_card.png') + ')'
                    break;
                default:
                    break;
            }
        },
        
        /* Update the cost text color (e.g. x6) to pink if the user has enough affinity
         or green if the user has enough runes + affinity to buy the card
        */
        updateCardCostColors: function() {
            this.users.forEach( (user) => {
                if (user.sid == this.currentTurnSid) {
                    console.log("update card cost user sid: " + user.sid)
                    if (this.cost.FIRE - user.affinities.FIRE <= 0) { // if the user has enough affinity in this rune type to buy it for free
                         this.$refs.fireCost.style.color = "#dd42f5" 
                    } else if (this.cost.FIRE - user.affinities.FIRE - user.runes.FIRE <= 0)  { // otherwise, if the user can afford it with affinity and the runes they own
                        this.$refs.fireCost.style.color = "#66bb6a"
                    } else if (this.cost.FIRE - user.affinities.FIRE - user.runes.FIRE >= 0) { // otherwise, if they don't have enough affinity or runes
                        this.$refs.fireCost.style.color = "#ffffff"
                    }

                    if (this.cost.NATURE - user.affinities.NATURE <= 0) { 
                        this.$refs.natureCost.style.color  = "#dd42f5" 
                    } else if (this.cost.NATURE - user.affinities.NATURE - user.runes.NATURE <= 0)  { 
                        this.$refs.natureCost.style.color  = "#66bb6a"
                    } else if (this.cost.NATURE - user.affinities.NATURE - user.runes.NATURE >= 0) { 
                        this.$refs.natureCost.style.color = "#ffffff"
                    }
                    
                    if (this.cost.WATER - user.affinities.WATER <= 0) {
                        this.$refs.waterCost.style.color  = "#dd42f5"
                    } else if (this.cost.WATER - user.affinities.WATER - user.runes.WATER <= 0)  {
                        this.$refs.waterCost.style.color  = "#66bb6a"
                    } else if (this.cost.WATER - user.affinities.WATER - user.runes.WATER >= 0) {
                        this.$refs.waterCost.style.color = "#ffffff"
                    }

                    if (this.cost.EARTH - user.affinities.EARTH <= 0) {
                        this.$refs.earthCost.style.color  = "#dd42f5"
                    } else if (this.cost.EARTH - user.affinities.EARTH - user.runes.EARTH <= 0)  {
                        this.$refs.earthCost.style.color  = "#66bb6a"
                    } else if (this.cost.EARTH - user.affinities.EARTH - user.runes.EARTH >= 0) {
                        this.$refs.earthCost.style.color = "#ffffff"
                    }
                    
                    if (this.cost.ARCANE - user.affinities.ARCANE <= 0) {
                        this.$refs.arcaneCost.style.color  = "#dd42f5"
                    } else if (this.cost.ARCANE - user.affinities.ARCANE - user.runes.ARCANE <= 0)  {
                        this.$refs.arcaneCost.style.color  = "#66bb6a"
                    } else if (this.cost.ARCANE - user.affinities.ARCANE - user.runes.ARCANE >= 0) {
                        this.$refs.arcaneCost.style.color = "#ffffff"
                    }

                    if (this.cost.WIND - user.affinities.WIND <= 0) {
                        this.$refs.windCost.style.color  = "#dd42f5"
                    } else if (this.cost.WIND - user.affinities.WIND - user.runes.WIND <= 0)  {
                        this.$refs.windCost.style.color  = "#66bb6a"
                    } else if (this.cost.WIND - user.affinities.WIND - user.runes.WIND >= 0) {
                        this.$refs.windCost.style.color = "#ffffff"
                    }

                    if (this.cost.DARK - user.affinities.DARK <= 0) {
                        this.$refs.darkCost.style.color  = "#dd42f5"
                    } else if (this.cost.DARK - user.affinities.DARK - user.runes.DARK <= 0)  {
                        this.$refs.darkCost.style.color  = "#66bb6a"
                    } else if (this.cost.DARK - user.affinities.DARK - user.runes.DARK >= 0) {
                        this.$refs.darkCost.style.color = "#ffffff"
                    }
    
                    if (this.cost.SOLAR - user.affinities.SOLAR <= 0) {
                        this.$refs.solarCost.style.color = "#dd42f5"
                    } else if (this.cost.SOLAR - user.affinities.SOLAR - user.runes.SOLAR <= 0)  {
                        this.$refs.solarCost.style.color  = "#66bb6a"
                    } else if (this.cost.SOLAR - user.affinities.SOLAR - user.runes.SOLAR >= 0) {
                        this.$refs.solarCost.style.color = "#ffffff"
                    }
                }
            });
        }
    },

    created: function() {
        
    },

    mounted: function() {
        this.updateCardBtnBackground()
    },

    updated: function() {
        this.updateCardBtnBackground()
        this.updateCardCostColors()
    }
};
</script>
  
<style scoped>
    .idvalue {
    color: #ffffff;
    font-weight: bold;
    font-size: min(1.5vw, 15px);
    
    }

    .damage-type-image-stats{
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .damage-value {
        color: white;
        padding-left: 3px;
        font-size: min(3vw, 15px);
    }
    


    .tooltip-cardshop {
        position: relative;
    }

    .tooltip-cardshop:before {
        content: attr(data-hover);
        visibility: hidden;
        opacity: 0;
        width: 88px;
        height: max-content;

        border-radius: .3rem;
        background-color: rgb(25, 25, 25);
        color: #fff;
        text-align: center;
        padding: 5px 0;
        transition: opacity .55s ease-in-out;
        
        position: absolute;
        
        top: -.25rem;
        left: 50%;
        transform: translateX(-50%) translateY(-100%);
       
        padding: .5rem;
    }

    /* Render hover tooltip on hover */
    .tooltip-cardshop:hover:before {
        opacity: 1;
        visibility: visible;
    }






    .affinity-stats {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;

    }

    .affinity-value {
        color: white;
        padding-left: 3px;
        font-size: min(3vw, 15px);
    }


    .card-button {
        height: 100%;
        width: 100%;
        max-height: 5vh;
        min-height: 10em;
        
        background-color: #2b3849;
        border-radius: 1rem;
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        align-items: center;
        justify-items: center;
        cursor: pointer;
    }

    .card-button:active {
        transform: translateY(1px);
        opacity: 70%;
    }

    .cost-icons {
        width:100%; 
        max-width: 2em; 
        max-height: 2em; 
        height: 100%;
    }

    /* COST GRID CONTAINER STYLING */
    .icon-text-container {
        display: flex;
    }

    .text {
        padding-right: .2em;
        color: white;
        margin-top: .25rem;
        width: 1.5em;
        text-align: right;
        font-size: min(1.5vw, 15px);
    }

    
    .cost-container {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
        padding: 5px;
        justify-items: center;
    }

    /* MOBILE */
    @media screen and (max-width: 768px) {

        .parent-container {
            justify-content: center;
            align-items: center;
            display: flex;
            flex-direction: column;
        }

        .idvalue {
            color: #ffffff;
            font-weight: bold;
            font-size: min(4vw, 15px);
        
        }
        .card-button {
            background-color: #2b3849;
            border-radius: 1rem;
            width: 100%;
            height: 100%;
            min-height: 10em;
            max-width: 25em;
        }

        .cost-container {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            padding: 5px;
            width: 25em;
            justify-items: center;
        }

        .cost-icons {
            width:100%; 
            max-width: 2em; 
            max-height: 2em; 
            height: 100%;
        }

        .text {
            padding-right: .2em;
            color: white;
            margin-top: .25rem;
            width: 1.5em;
            text-align: right;
            font-size: min(10vw, 15px);
        }
        
        .tooltip-cardshop:before{
            content: none;
        }


    }

</style>