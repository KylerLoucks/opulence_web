<template>

    <div ref="playerCardButton" class="card-button"> 

        <div class="damage-type-image-stats">
            <span class="tooltip-cardshop" data-hover="Attack Card" v-if="spellType == 'ATTACK'"><img draggable="false" src="@/assets/sword.png" style="width:100%; max-width: 32px; max-height: 32px; height: 100%;"/></span>
            <span class="tooltip-cardshop" data-hover="Defence Card" v-else-if="spellType == 'SHIELD'" ><img draggable="false" src="@/assets/shield.png" style="width:100%; max-width: 32px; max-height: 32px; height: 100%;"/></span> 
            <span class="tooltip-cardshop" data-hover="Mundane" v-else> <img draggable="false" src="@/assets/mundane.png" style="width:100%; max-width: 32px; max-height: 32px; height: 100%;"/></span>
            <h3 class="damage-value">{{power}}</h3>
        </div>

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
    </div>

</template>
  
  
<script>
    export default {
    name: "CardsInHand",
   
    props: { // variables when instantiating this component
        cost: Object,
        affinity: Number,
        power: Number,
        runeType: String,
        spellType: String,
    },
    setup() {
        return {
        };
    },

    methods: {
        updateCardBtnBackground: function() {
            var element = this.$refs.playerCardButton;
            element.style.backgroundRepeat = "no-repeat"
            element.style.backgroundSize = "100% 160px"
            element.style.backgroundAttachment = "fixed"

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
    },

    created: function() {
    },

    mounted: function() {
        this.updateCardBtnBackground()
    },

    updated: function() {
        this.updateCardBtnBackground()
    }
};
</script>
  
<style scoped>

    .damage-type-image-stats{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
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
    }

    .affinity-value {
        color: white;
        padding-left: 3px;
        font-size: min(3vw, 15px);
    }


    .card-button {
        height: 100%;
        width: 100%;
        min-height: 5em;
        background-color: #2b3849;
        border-radius: 1rem;
        box-shadow: 0px 5px 20px #888888;
        display: grid;
        grid-template-columns: 1fr 1fr;
        justify-content: center;
    }
    /* MOBILE */
    @media screen and (max-width: 740px) {
    }

</style>