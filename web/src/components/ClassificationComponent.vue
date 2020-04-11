<template>
<div class="col-md-2 left_side">
  <div class="inCloset">
    <b-dropdown id="dropdown-dropright" dropright variant="outline-info" v-for="category in list" v-bind:text="category.name" class="m-2" size="lg" v-bind:key="category.name">
      <b-dropdown-item v-for="detail in category.details" v-bind:key="detail" href="#">
        {{ detail }}
      </b-dropdown-item>
    </b-dropdown>
  </div>
</div>
</template>
<script>
export default {
  name: 'ClassificationComponent',
  props: ['list']

}
</script>

<style scoped>
.left_side{
    display: inline-block;
}

.m-2 {
    width: 105.1px;
}
</style>
