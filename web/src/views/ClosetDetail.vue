<template>
  <div class="closet_detail">
      <div class="container_1">
          <MainNavigation></MainNavigation>
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
import MainNavigation from '@/components/MainNavigation.vue'
export default {
  name: 'ClosetDetail',
  components: {
    ClosetDetailComponent,
    ClosetModifiedComponent,
    ClosetDeletedComponent,
    MainNavigation

  }

}
</script>

<style>
.closet_detail{
    width: 100%;
    margin-right: auto;
    margin-left: auto;
}
</style>
