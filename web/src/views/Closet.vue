<template>
    <div id="Closet">
        <HomeNavigation></HomeNavigation>
        <ClosetComponent></ClosetComponent>
        <ClassificationComponent></ClassificationComponent>
    </div>
</template>

<script>
import ClosetComponent from '@/components/ClosetComponent.vue'
import ClassificationComponent from '@/components/ClassificationComponent.vue'
export default {
  name: 'Closet',
  components: {
    ClosetComponent,
    ClassificationComponent
  }

}
</script>
<style>

</style>
