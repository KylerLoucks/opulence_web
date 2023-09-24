<template>

    <div ref="chat" class="chat-container">
        <div class="log-container" v-for="(log) in logs" :key="log">
            <p ref="gameLogs" class="log-text">{{log}}</p>
        </div>
    </div>
    
</template>
  
  
<script>

    
    export default {
    name: "ChatLogs",
   
    props: { // variables when instantiating this component
        logs: Array,
    },
    setup() {
        return {
        };
    },
    data: function() {
        return {

        }
    },

    methods: {
        scrollChatLogToEnd() {
          // var container = document.querySelector(".chat-log-container")
          var container = this.$refs.chat
          if(container) {
            container.scrollTop = container.scrollHeight;
          }
        },


        /**
         * Returns an <img html element with the image specified
         * @param {*} imgName the name of the image (e.g. skull => skull.png)
         */
        genImgElement: function(imgName) {
            var img = new Image();
            img.className = "emojified";
            img.style.width = '100%';
            img.style.width = '100%';
            img.style.maxWidth = '1.5em'
            img.style.maxHeight = '1.5em'
            img.style.transform = "translateY(.2em)";
            img.setAttribute('draggable', 'false');
            img.src = require(`@/assets/${imgName}.png`); // @ is the equivilant of /src
            return img.outerHTML
        },

        /**
         * Replaces innerHTML text with an outer <img> html element returned from genImgElement
         */
        regexReplaceInnerHTML: function() {
            var mapObj = {
                ":arcane:": this.genImgElement("ARCANE"),
                ":fire:":this.genImgElement("FIRE"),
                ":water:":this.genImgElement("WATER"),
                ":nature:":this.genImgElement("NATURE"),
                ":earth:":this.genImgElement("EARTH"),
                ":dark:":this.genImgElement("DARK"),
                ":wind:":this.genImgElement("WIND"),
                ":solar:":this.genImgElement("SOLAR"),
                ":skull:":this.genImgElement("death"),
            }
            var reg = new RegExp(Object.keys(mapObj).join("|"), "g") // outputs as regex: /:arcane:|:fire:/g from obj keys in mapObj
            var elements = this.$refs.gameLogs // refs within v-for return a list of html elements
            for (let i = 0; i < elements.length; i++) {
                elements[i].innerHTML = elements[i].innerHTML.replace(reg, function(matched) {return mapObj[matched]});
            }
        }
    },

    created: function() { // debugging the props
        // console.log(this.logs)

    },

    mounted: function() {
        this.regexReplaceInnerHTML()
    },

    updated: function() {
        this.regexReplaceInnerHTML()
        this.scrollChatLogToEnd();
    }
};
</script>
  
<style scoped>

    .chat-container {
        overflow: auto;
        overflow-x: hidden;
    }
    .log-container {
        margin-left: .2em;
    }

    .log-text {
    text-align: left;
    /* margin: 2px; */
    color: white;
    font-family: monospace;
    font-size: min(2vw, 14px);
    }

    /* @media screen and (max-width: 740px) {
        .log-text {
            text-align: left;
            color: white;
            font-family: monospace;
            font-size: min(1.5vw, 14px);
        }
    } */


    .emojified {
    height: 1.25em;
    width: 1.25em;
    padding: 0 .05em 0 .1em;
    vertical-align: -0.2em;
    }

    /* MOBILE */
    @media screen and (max-width: 768px) {
        .log-text {
            text-align: left;
            /* margin: 2px; */
            color: white;
            font-family: monospace;
            font-size: min(3vw, 14px);
        }
    }




</style>