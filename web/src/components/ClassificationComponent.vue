<template>
  <b-container>
    <b-dropdown id="dropdown-dropright"
                dropright
                variant="outline-info"
                v-for="category in list"
                v-bind:key="category.upper"
                v-bind:text="category.upper"
                class="m-2"
                size="lg">
      <b-dropdown-item v-for="detail in category.lower"
                        v-bind:key="detail"
                        @click="$emit('chooseCategory', category.upper, detail)">
        {{ detail }}
      </b-dropdown-item>
    </b-dropdown>
  </b-container>
</template>
<script>
export default {
  name: 'ClassificationComponent',
  props: [
    'list'
  ]
}
</script>

<style>

</style>
