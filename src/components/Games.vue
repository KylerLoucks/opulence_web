<template>

    <button class="container" v-on:click="$emit('joinRoom', joinRoom)">
        <div class="game-data-container">
            <span class="idvalue">Game ID: {{id}}</span>
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
        started: Boolean,
    },
    setup() {
        return {
            
        };
    },
    created: function() { // debugging the props
        console.log(this.users)
    }
};
</script>
  
<style scoped>
    .container {
    height: max-content;
    
    width: 25em;
    height: 70px;
    background-color: #515862;
    border-radius: .25rem;

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