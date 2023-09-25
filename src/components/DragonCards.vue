<template>
    <div class="parent-container">
        <button class="card-button" v-on:click="$emit('buyDragon', buyDragon)">
            <div class="card-stats-container">
                    <img v-if="dragonType == 'THORN'" class="dragon-image" :src="dragonIconPath('Thorn_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'CRYSTAL'" class="dragon-image" :src="dragonIconPath('Crystal_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'DEEP-SEA'" class="dragon-image" :src="dragonIconPath('Deep-sea_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'DUST'" class="dragon-image" :src="dragonIconPath('Dust_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'LAVA'" class="dragon-image" :src="dragonIconPath('Lava_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'LUNAR'" class="dragon-image" :src="dragonIconPath('Lunar_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'MUD'" class="dragon-image" :src="dragonIconPath('Mud_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'NOVA'" class="dragon-image" :src="dragonIconPath('Nova_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'SMOKE'" class="dragon-image" :src="dragonIconPath('Smoke_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'STEAM'" class="dragon-image" :src="dragonIconPath('Steam_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'STELLAR'" class="dragon-image" :src="dragonIconPath('Stellar_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'SWAMP'" class="dragon-image" :src="dragonIconPath('Swamp_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'VOID'" class="dragon-image" :src="dragonIconPath('Void_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <img v-else-if="dragonType == 'CLOUD'" class="dragon-image" :src="dragonIconPath('Cloud_Dragon.png')" style="" draggable="false" data-hover="Mundane"/>
                    <h3 class="idvalue">{{dragonType}} DRAGON</h3>
            </div>
        </button>

        
        <div class="cost-container">
            <div v-if="cost.SOLAR" class="icon-text-container">
                <h3 ref="solarCost" class="text">x{{cost.SOLAR}}</h3>
                <img draggable="false" src="@/assets/SOLAR.png" style="width: 32px; height: 32px;"/>
            </div>
            <div v-if="cost.WATER" class="icon-text-container">
                <h3 ref="waterCost" class="text">x{{cost.WATER}}</h3>
                <img draggable="false" src="@/assets/WATER.png" style="width: 32px; height: 32px;"/>
            </div>
            <div v-if="cost.ARCANE" class="icon-text-container">
                <h3 ref="arcaneCost" class="text">x{{cost.ARCANE}}</h3>
                <img draggable="false" src="@/assets/ARCANE.png" style="width: 32px; height: 32px;"/>
            </div>
            <div v-if="cost.WIND" class="icon-text-container">
                <h3 ref="windCost" class="text">x{{cost.WIND}}</h3>
                <img draggable="false" src="@/assets/WIND.png" style="width: 32px; height: 32px;"/>
            </div>
            <div v-if="cost.FIRE" class="icon-text-container">
                <h3 ref="fireCost" class="text">x{{cost.FIRE}}</h3>
                <img draggable="false" src="@/assets/FIRE.png" style="width: 32px; height: 32px;"/>
            </div>
            <div v-if="cost.NATURE" class="icon-text-container">
                <h3 ref="natureCost" class="text">x{{cost.NATURE}}</h3>
                <img draggable="false" src="@/assets/NATURE.png" style="width: 32px; height: 32px;"/>
            </div>
            <div v-if="cost.DARK" class="icon-text-container">
                <h3 ref="darkCost" class="text">x{{cost.DARK}}</h3>
                <img draggable="false" src="@/assets/DARK.png" style="width: 32px; height: 32px;"/>
            </div>
            <div v-if="cost.EARTH" class="icon-text-container">
                <h3 ref="earthCost" class="text">x{{cost.EARTH}}</h3>
                <img draggable="false" src="@/assets/EARTH.png" style="width: 32px; height: 32px;"/>
            </div>
        </div>
    </div>
</template>
  
  
<script>
    export default {
    name: "DragonCards",
   
    props: { // variables when instantiating this component
        cost: Object,
        dragonType: String,
        users: Array,
        currentTurnSid: String,
        
    },
    setup() {
        return {
        };
    },

    methods: {
        dragonIconPath(value) {
        return require(`@/assets/dragons/${value}`)
        },

            /* Update the cost text color (e.g. x6) to pink if the user has enough affinity
         or green if the user has enough runes + affinity to buy the card
        */
        updateCardCostColors: function() {
            this.users.forEach( (user) => {
                if (user.sid == this.currentTurnSid) {
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
    },

    updated: function() {
        this.updateCardCostColors()
    }
};
</script>
  
<style scoped>
    .idvalue {
    color: white;
    font-weight: bold;
    font-size: 15px;
    
    }

    .card-button {
    background-color: #2b3849;
    border-radius: 1rem;
    width: 19em;
    height: 238px;
    cursor: pointer;
    }

    .card-button:active {
    transform: translateY(1px);
    opacity: 70%;
    }

    .card-stats-container {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        
        justify-items: center;
        align-items: center;
    }

    .dragon-image {
        border-radius: .75em;
        width: 100%; 
        height: 186px;
        margin-top: .2em;
    }

    /* needs to be a SPAN or DIV to work */
    .dragon-image:before {
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


    .icon-text-container {
        display: flex;
    }

    .text {
        padding-right: .2em;
        color: white;
        margin-top: .25rem;
        width: 1.5em;
        text-align: right;
    }

    .cost-icons {
        width:100%; 
        max-width: 2em; 
        max-height: 2em; 
        height: 100%;
    }

    .cost-container {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
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
            min-height: 5em;
            max-height: 20em;
            max-width: 25em;
        }

        .cost-icons {
            width:100%; 
            max-width: 1em; 
            max-height: 1em; 
            height: 100%;
        }
        
        .tooltip-cardshop:before{
            content: none;
        }

        .dragon-image {
            border-radius: .75em;
            width: 100%; 
            height: 200px;
            margin-top: .2em;
        }

        .cost-container {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            padding: 5px;
            width: 25em;
            justify-items: center;
        }
    }




</style>