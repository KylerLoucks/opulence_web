<template>

    

    <button class="container" v-on:click="$emit('joinRoom', id.replace('GAME#', ''))">
        <div class="game-data-container">
            <div class="idvalue">Game ID: {{ id ? id.replace('GAME#', '') : ''}}</div>
            <div class="startedvalue">Started: {{started}}</div>
            <div class="idvalue">Players: {{ players }}</div>
            <!-- <div class="total-users-container">
                <span class="total-users">Users:</span> 
                <div class="total-users" v-for="user in users" :key="user" >
                    <span>{{user}}</span>
                </div>
            </div> -->
        </div> 
        
        
    </button>
</template>
  
  
<script>

    export default {
    name: "PlayableGames",
   
    props: { // variables when instantiating this component
        id: String,
        players: Number,
        started: String,
    },
    setup() {
        return {
            
        };
    },
    created: function() { // debugging the props
        console.log(this.players)
    },

    updated: function() {
        
    }
};
</script>
  
<style scoped>


    .container {
    height: max-content;
    
    width: 100%;
    height: 10em;
    background: transparent;
    border-radius: .25rem;
    transition: 1s;
    padding: 10px 30px;
    letter-spacing: .1em;

    }

    .container:hover {
        background: linear-gradient(to top, #ffffff39, rgba(255, 255, 255, 0.319));
        letter-spacing: 0.2em;
        box-shadow: 0 10px 25px #7c21f4;
    }

    .game-data-container {
        display: flex;
        flex-wrap: wrap;
        grid-template-columns: 4fr 1fr 1fr;
        width: 100%;
        height: 100%;
        justify-items: center;
        align-items: center;
    }

    .total-users-container {
        display: flex;
        overflow: auto;
        margin-top: 10px;
    }


    .total-users {
        color: White;
        font-weight: bold;
        display: flex;
        margin: 5px;
        font-size: .75em;
    }
    
    .idvalue {
    color: white;
    font-weight: bold;
    margin: 5px;
    }

    .startedvalue {
    color: white;
    font-weight: bold;
    margin: 10px;
    }
</style>