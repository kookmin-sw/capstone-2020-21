<template>
  <div class="closet_detail">
      <div class="container_1">
          <div class="row">
              <ClosetDetailComponent></ClosetDetailComponent>
              <ClosetModifiedComponent></ClosetModifiedComponent>
              <ClosetDeletedComponent></ClosetDeletedComponent>
          </div>
      </div>
  </div>
</template>

<script>
import ClosetDetailComponent from '@/components/ClosetDetailComponent.vue'
import ClosetModifiedComponent from '@/components/ClosetModifiedComponent.vue'
import ClosetDeletedComponent from '@/components/ClosetDeletedComponent.vue'
export default {
  name: 'ClosetDetail',
  components: {
    ClosetDetailComponent,
    ClosetModifiedComponent,
    ClosetDeletedComponent

  }

}
</script>

<style>

</style>
