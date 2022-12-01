<template>
    <div class="parent-container">
        <div class="cost-container">
                <img v-on:click="canAffordFire ? runeClicked('FIRE') : ''" :class="canAffordFire ? 'runes' : 'cant-afford'" draggable="false" src="@/assets/FIRE.png" style="width: 100%; height: 100%; max-width: 3em; max-height: 3em;"/>
                <img v-on:click="canAffordWater ? runeClicked('WATER') : ''" :class="canAffordWater ? 'runes' : 'cant-afford'" draggable="false" src="@/assets/WATER.png" style="width: 100%; height: 100%; max-width: 3em; max-height: 3em;"/>
                <img v-on:click="canAffordEarth ? runeClicked('EARTH') : ''" :class="canAffordEarth ? 'runes' : 'cant-afford'" draggable="false" src="@/assets/EARTH.png" style="width: 100%; height: 100%; max-width: 3em; max-height: 3em;"/>
                <img v-on:click="canAffordArcane ? runeClicked('ARCANE') : ''" :class="canAffordArcane ? 'runes' : 'cant-afford'" draggable="false" src="@/assets/ARCANE.png" style="width: 100%; height: 100%; max-width: 3em; max-height: 3em;"/>
                <img v-on:click="canAffordNature ? runeClicked('NATURE') : ''" :class="canAffordNature ? 'runes' : 'cant-afford'" draggable="false" src="@/assets/NATURE.png" style="width: 100%; height: 100%; max-width: 3em; max-height: 3em;"/>
                <img v-on:click="canAffordSolar ? runeClicked('SOLAR') : ''" :class="canAffordSolar ? 'runes' : 'cant-afford'" draggable="false" src="@/assets/SOLAR.png" style="width: 100%; height: 100%; max-width: 3em; max-height: 3em;"/>
                <img v-on:click="canAffordDark ? runeClicked('DARK') : ''" :class="canAffordDark ? 'runes' : 'cant-afford'" draggable="false" src="@/assets/DARK.png" style="width: 100%; height: 100%; max-width: 3em; max-height: 3em;"/>
                <img v-on:click="canAffordWind ? runeClicked('WIND') : ''" :class="canAffordWind ? 'runes' : 'cant-afford'" draggable="false" src="@/assets/WIND.png" style="width: 100%; height: 100%; max-width: 3em; max-height: 3em;"/>
        </div>

        <div class="selected-runes-container">
            <div class="selected-rune1">
                <img v-show="rune1Clicked" ref="selected1" v-on:click="unClickSlot(1)" draggable="false" src="@/assets/NATURE.png" style="width: 100%; height: 100%;"/>               
            </div>
            <div class="selected-rune2">
                <img ref="selected2" v-show="rune2Clicked" v-on:click="unClickSlot(2)" draggable="false" src="@/assets/NATURE.png" style="width: 100%;  height: 100%;"/>
            </div>
        </div>

        

        <div class="craft-button-container">
            <button class="reset-button" v-on:click="resetSelectedRunes()">RESET</button>
            <button :class="rune1Clicked && rune2Clicked ? 'craft-button' : 'craft-button-grayed'" v-on:click="$emit('craftCard', rune1, rune2), resetSelectedRunes()">CRAFT</button>
        </div>

</div>
    

</template>
  
  
<script>
    export default {
    name: "CraftingCards",
   
    props: { // variables when instantiating this component
        users: Array,
        currentTurnSid: String,
        
    },
    // instanciate things when the component is used
    setup() {
        return {
        };
    },

    data: function() {
        return {
            canAffordFire: false,
            canAffordWater: false,
            canAffordEarth: false,
            canAffordNature: false,
            canAffordArcane: false,
            canAffordSolar: false,
            canAffordDark: false,
            canAffordWind: false,
            rune1Clicked: false, 
            rune2Clicked: false,
            rune1: 'none',
            rune2: 'none'
        }
    },

    methods: {
        runeClicked(element) {
            console.log(element)

            if (element == this.rune1 || element == this.rune2) return;
            
            if (!this.rune1Clicked) {
                this.rune1Clicked = true
                console.log(this.rune1Clicked)
                this.$refs.selected1.src = require(`@/assets/${element}.png`)
                this.rune1 = element;
                
            } else if (!this.rune2Clicked) {
                this.rune2Clicked = true
                this.$refs.selected2.src = require(`@/assets/${element}.png`)
                this.rune2 = element;
            }
        },

        resetSelectedRunes() {
            this.rune1Clicked = false
            this.rune2Clicked = false
            this.rune1 = 'none'
            this.rune2 = 'none'
        },

        unClickSlot(index) {
            if (index == 1) {
                this.rune1Clicked = false;
                this.rune1 = 'none';
            }
            else if (index == 2) {
                this.rune2Clicked = false;
                this.rune2 = 'none';
            }
        },

        activateRunes() {
            this.users.forEach( (user) => {
                if (user.sid == this.currentTurnSid) {
                    console.log("update crafting cost for user sid: " + user.sid)
                    if (user.runes.FIRE + user.affinities.FIRE < 2) {
                        this.canAffordFire = false;
                    } else {
                        this.canAffordFire = true;
                    }
                    if (user.runes.WATER + user.affinities.WATER < 2) {
                        this.canAffordWater = false;
                    } else {
                        this.canAffordWater = true;
                    }
                    if (user.runes.EARTH + user.affinities.EARTH < 2) {
                        this.canAffordEarth = false;
                    } else {
                        this.canAffordEarth = true;
                    }
                    if (user.runes.NATURE + user.affinities.NATURE < 2) {
                        this.canAffordNature = false;
                    } else {
                        this.canAffordNature = true;
                    }
                    if (user.runes.ARCANE + user.affinities.ARCANE < 2) {
                        this.canAffordArcane = false;
                    } else {
                        this.canAffordArcane = true;
                    }
                    if (user.runes.DARK + user.affinities.DARK < 2) {
                        this.canAffordDark = false;
                    } else {
                        this.canAffordDark = true;
                    }
                    if (user.runes.WIND + user.affinities.WIND < 2) {
                        this.canAffordWind = false;
                    } else {
                        this.canAffordWind = true;
                    }
                    if (user.runes.SOLAR + user.affinities.SOLAR < 2) {
                        this.canAffordSolar = false;
                    } else {
                        this.canAffordSolar = true;
                    }
                }
            });
        },
    },

    created: function() {
    },

    mounted: function() {
        this.activateRunes()
    },

    updated: function() {
        this.activateRunes()
    }
};
</script>
  
<style scoped>

    .runes:active {
    transform: translateY(1px);
    opacity: 70%;
    }

    .craft-button {
        color: white;
        background-color: #4fa947;
        border: 2px solid #31672c;
        margin: 12px;
        font-size: 18px;
        border-radius: 6px;
    }

    .craft-button:active {
        transform: translateY(1px);
        opacity: 70%;        
    }

    .craft-button-grayed {
        color: rgba(255, 255, 255, 0.553);
        background-color: #3b523778;
        border: 2px solid #21332185;
        margin: 12px;
        font-size: min(3vw, 18px);
        border-radius: 6px;
    }

    .reset-button {
        color: white;
        background-color: #a94747;
        border: 2px solid #5e2828;
        margin: 12px;
        font-size: min(3vw, 18px);
        border-radius: 6px;
    }

    .reset-button:active {
        transform: translateY(1px);
        opacity: 70%;
    }

    .craft-button-container {
        justify-content: center;
    }

    .selected-runes-container {
        display: flex;
        justify-content: center;
    }

    .selected-rune1, .selected-rune2 {
        height: 2vmax;
        width:  2vmax;
        background-color: rgb(47, 47, 47);
        border-radius: 6px;
        border: .2rem solid #d9d9d9;
        margin: .3rem;
    }

    .cant-afford {
        opacity: 35%;
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
    
    .cost-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    padding: 5px;
    justify-items: center;
    
    
    }


</style>