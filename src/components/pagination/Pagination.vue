<template>
    <ul :class="containerClass" v-if="!noLiSurround">
  
      <!-- First page button -->
      <li v-if="firstLastButton" :class="[pageClass, firstPageSelected() ? disabledClass : '']">
        <a @click="selectFirstPage()" @keyup.enter="selectFirstPage()" :class="firstLastClass" :tabindex="firstPageSelected() ? -1 : 0" v-html="firstButtonText"></a>
      </li>
  
      <!-- prev page button -->
      <li v-if="!(firstPageSelected() && hidePrevNext)" :class="[prevClass, firstPageSelected() ? disabledClass : '']">
        <a @click="prevPage()" @keyup.enter="prevPage()" :class="prevLinkClass" :tabindex="firstPageSelected() ? -1 : 0" v-html="prevText"></a>
      </li>
  
      <!-- Number buttons -->
      <li v-for="page in pages" :key="page" :class="[pageClass, page.selected ? activeClass : '', page.disabled ? disabledClass : '', page.breakView ? breakViewClass: '']">
        <a v-if="page.breakView" :class="[pageLinkClass, breakViewLinkClass]" tabindex="0"><slot name="breakViewContent">{{ breakViewText }}</slot></a>
        <a v-else-if="page.disabled" :class="pageLinkClass" tabindex="0">{{ page.content }}</a>
        <a v-else @click="handlePageSelected(page.index + 1)" @keyup.enter="handlePageSelected(page.index + 1)" :class="pageLinkClass" tabindex="0">{{ page.content }}</a>
      </li>
  
      <!-- next page button -->
      <li v-if="!(lastPageSelected() && hidePrevNext)" :class="[nextClass, lastPageSelected() ? disabledClass : '']">
        <a @click="nextPage()" @keyup.enter="nextPage()" :class="nextLinkClass" :tabindex="lastPageSelected() ? -1 : 0" v-html="nextText"></a>
      </li>
  
      <!-- Last page button -->
      <li v-if="firstLastButton" :class="[pageClass, lastPageSelected() ? disabledClass : '']">
        <a @click="selectLastPage()" @keyup.enter="selectLastPage()" :class="firstLastClass" :tabindex="lastPageSelected() ? -1 : 0" v-html="lastButtonText"></a>
      </li>
    </ul>

    


    <div :class="containerClass" v-else>
      <button v-if="firstLastButton" @click="selectFirstPage()" @keyup.enter="selectFirstPage()" :class="[pageLinkClass, firstPageSelected() ? disabledClass : '']" tabindex="0" v-html="firstButtonText"></button>
      <button v-if="!(firstPageSelected() && hidePrevNext)" @click="prevPage()" @keyup.enter="prevPage()" :class="['page-buttons', firstPageSelected() ? disabledClass : '']" tabindex="0" v-html="prevText"></button>
      
      <template v-for="page in pages" :key="page">
        <button v-if="page.breakView" :class="['page-buttons', breakViewLinkClass, page.disabled ? disabledClass : '']" tabindex="0"><slot name="breakViewContent">{{ breakViewText }}</slot></button>
        <button v-else-if="page.disabled" :class="['page-buttons', page.selected ? 'page-buttons-active' : '', disabledClass]" tabindex="0">{{ page.content }}</button>
        <button v-else @click="handlePageSelected(page.index + 1)" @keyup.enter="handlePageSelected(page.index + 1)" :class="['page-buttons', page.selected ? 'page-buttons-active' : '']" tabindex="0">{{ page.content }}</button>
      </template>

      <button v-if="!(lastPageSelected() && hidePrevNext)" @click="nextPage()" @keyup.enter="nextPage()" :class="['page-buttons', lastPageSelected() ? disabledClass : '']" tabindex="0" v-html="nextText"></button>
      <button v-if="firstLastButton" @click="selectLastPage()" @keyup.enter="selectLastPage()" :class="['page-buttons', lastPageSelected() ? disabledClass : '']" tabindex="0" v-html="lastButtonText"></button>
    </div>
  </template>
  
  <script>
  export default {
    name: "PageList",
    props: {
      value: {
        type: Number
      },
      pageCount: {
        type: Number,
        required: true
      },
      forcePage: {
        type: Number
      },
      clickHandler: {
        type: Function,
        default: () => { }
      },
      pageRange: {
        type: Number,
        default: 3
      },
      marginPages: {
        type: Number,
        default: 1
      },
      prevText: {
        type: String,
        default: 'Prev'
      },
      nextText: {
        type: String,
        default: 'Next'
      },
      breakViewText: {
        type: String,
        default: '…'
      },
      containerClass: {
        type: String
      },
      firstLastClass: {
        type: String
      },
      pageClass: {
        type: String
      },
      pageLinkClass: {
        type: String
      },
      prevClass: {
        type: String
      },
      prevLinkClass: {
        type: String
      },
      nextClass: {
        type: String
      },
      nextLinkClass: {
        type: String
      },
      breakViewClass: {
        type: String
      },
      breakViewLinkClass: {
        type: String
      },
      activeClass: {
        type: String,
        default: 'active'
      },
      disabledClass: {
        type: String,
        default: 'disabled'
      },
      noLiSurround: {
        type: Boolean,
        default: false
      },
      firstLastButton: {
        type: Boolean,
        default: false
      },
      firstButtonText: {
        type: String,
        default: 'First'
      },
      lastButtonText: {
        type: String,
        default: 'Last'
      },
      hidePrevNext: {
        type: Boolean,
        default: false
      }
    },
    beforeUpdate() {
      if (this.forcePage === undefined) return
      if (this.forcePage !== this.selected) {
        this.selected = this.forcePage
      }
    },
    computed: {
      selected: {
        get: function() {
          return this.value || this.innerValue
        },
        set: function(newValue) {
          this.innerValue = newValue
        }
      },
      pages: function () {
        let items = {}
        if (this.pageCount <= this.pageRange) {
          for (let index = 0; index < this.pageCount; index++) {
            let page = {
              index: index,
              content: index + 1,
              selected: index === (this.selected - 1)
            }
            items[index] = page
          }
        } else {
          const halfPageRange = Math.floor(this.pageRange / 2)
  
          let setPageItem = index => {
            let page = {
              index: index,
              content: index + 1,
              selected: index === (this.selected - 1)
            }
  
            items[index] = page
          }
  
          let setBreakView = index => {
            let breakView = {
              disabled: true,
              breakView: true
            }
  
            items[index] = breakView
          }
  
          // 1st - loop thru low end of margin pages
          for (let i = 0; i < this.marginPages; i++) {
            setPageItem(i);
          }
  
          // 2nd - loop thru selected range
          let selectedRangeLow = 0;
          if (this.selected - halfPageRange > 0) {
            selectedRangeLow = this.selected - 1 - halfPageRange;
          }
  
          let selectedRangeHigh = selectedRangeLow + this.pageRange - 1;
          if (selectedRangeHigh >= this.pageCount) {
            selectedRangeHigh = this.pageCount - 1;
            selectedRangeLow = selectedRangeHigh - this.pageRange + 1;
          }
  
          for (let i = selectedRangeLow; i <= selectedRangeHigh && i <= this.pageCount - 1; i++) {
            setPageItem(i);
          }
  
          // Check if there is breakView in the left of selected range
          if (selectedRangeLow > this.marginPages) {
            setBreakView(selectedRangeLow - 1)
          }
  
          // Check if there is breakView in the right of selected range
          if (selectedRangeHigh + 1 < this.pageCount - this.marginPages) {
            setBreakView(selectedRangeHigh + 1)
          }
  
          // 3rd - loop thru high end of margin pages
          for (let i = this.pageCount - 1; i >= this.pageCount - this.marginPages; i--) {
            setPageItem(i);
          }
        }
        return items
      }
    },
    data() {
      return {
        innerValue: 1,
      }
    },
    methods: {
      handlePageSelected(selected) {
        if (this.selected === selected) return
  
        this.innerValue = selected
        this.$emit('page-change', selected)
        this.clickHandler(selected)
      },
      prevPage() {
        if (this.selected <= 1) return
  
        this.handlePageSelected(this.selected - 1)
      },
      nextPage() {
        if (this.selected >= this.pageCount) return
  
        this.handlePageSelected(this.selected + 1)
      },
      firstPageSelected() {
        return this.selected === 1
      },
      lastPageSelected() {
        return (this.selected === this.pageCount) || (this.pageCount === 0)
      },
      selectFirstPage() {
        if (this.selected <= 1) return
  
        this.handlePageSelected(1)
      },
      selectLastPage() {
        if (this.selected >= this.pageCount) return
  
        this.handlePageSelected(this.pageCount)
      }
    }
  }
  </script>
  
  <style lang="css" scoped>
    :root {
      --main-bg-color: rgb(72, 218, 82);
    }

    button.page-buttons.page-buttons-active{
      background-color: #21f4bf73;
      margin-inline: 2px;
      box-shadow: 0 10px 25px #21f4bf;
    }

    .page-buttons{
      margin-inline: 5px;
      font-size: 1.5em;
      letter-spacing: 0.1em;
      padding: 10px 30px;
      color: #21f4bf;
      transition: 0.5s;
      border: none;
      background: transparent;
      border-style: solid;
      border-color: #4915cc #21f4bf;
      animation: rotate 5s infinite;
      border-radius: .5em;
    }
    @keyframes rotate {
      50%{
        border-color: #4915cc #21f4bf;
      }
      50% {
        border-color: #21f4bf #4915cc;
      }
    }
  
    .page-buttons:hover{
      cursor: pointer;
      letter-spacing: 0.25em;
      box-shadow: 0 10px 25px #21f4bf;
    }

  

  </style>
  