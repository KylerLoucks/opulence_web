<template>

    <button class="container" v-on:click="$emit('joinRoom', id.replace('GAME#', ''))">
        <div class="game-data-container">
            <span class="idvalue">Game ID: {{ id ? id.replace('GAME#', '') : ''}}</span>
            <span class="startedvalue">Started: {{started}}</span>
            <div class="total-users-container">
                <span class="total-users">Users:</span> 
                <div class="total-users" v-for="user in users" :key="user" >
                    <span>{{user}}</span>
                </div>
            </div>
        </div> 
        
        
    </button>
</template>
  
  
<script>

    export default {
    name: "PlayableGames",
   
    props: { // variables when instantiating this component
        id: String,
        users: Array,
        started: String,
    },
    setup() {
        return {
            
        };
    },
    created: function() { // debugging the props
        console.log(this.users)
    },

    updated: function() {
        
    }
};
</script>
  
<style scoped>
    .container {
    height: max-content;
    
    width: 25em;
    height: 170px;
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