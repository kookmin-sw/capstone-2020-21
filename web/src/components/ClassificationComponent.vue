<template>
<div class="col-md-2 left_side">
  <b-dropdown id="dropdown-dropright" dropright text="상의" variant="outline-info" class="m-2" size="lg">
      <b-dropdown-item href="?upper_category">전체</b-dropdown-item>
      <b-dropdown-item href="?upper_category=hoodie">후드티</b-dropdown-item>
      <b-dropdown-item href="#">반팔티셔츠</b-dropdown-item>
      <b-dropdown-item href="#">긴팔티셔츠</b-dropdown-item>
      <b-dropdown-item href="#">반팔셔츠</b-dropdown-item>
      <b-dropdown-item href="#">긴팔셔츠</b-dropdown-item>
      <b-dropdown-item href="#">맨투맨</b-dropdown-item>
      <b-dropdown-item href="#">터틀넥</b-dropdown-item>
      <b-dropdown-item href="#">니트</b-dropdown-item>
      <b-dropdown-item href="#">블라우스</b-dropdown-item>
      <b-dropdown-item href="#">끈나시</b-dropdown-item>
      <b-dropdown-item href="#">민소매</b-dropdown-item>

    </b-dropdown>
  <br/>
  <b-dropdown id="dropdown-dropright" dropright text="바지" variant="outline-info" class="m-2" size="lg">
      <b-dropdown-item href="#">전체</b-dropdown-item>
      <b-dropdown-item href="#">반바지</b-dropdown-item>
      <b-dropdown-item href="#">핫팬츠</b-dropdown-item>
      <b-dropdown-item href="#">슬랙스</b-dropdown-item>
      <b-dropdown-item href="#">청바지</b-dropdown-item>
      <b-dropdown-item href="#">골덴바지</b-dropdown-item>
      <b-dropdown-item href="#">트레이닝바지</b-dropdown-item>
    </b-dropdown>
  <br/>
  <b-dropdown id="dropdown-dropright" dropright text="치마" variant="outline-info" class="m-2" size="lg">
      <b-dropdown-item href="#">전체</b-dropdown-item>
      <b-dropdown-item href="#">미니스커트</b-dropdown-item>
      <b-dropdown-item href="#">롱스커트</b-dropdown-item>
    </b-dropdown>
  <br/>
  <b-dropdown id="dropdown-dropright" dropright text="아우터" variant="outline-info" class="m-2" size="lg">
      <b-dropdown-item href="#">전체</b-dropdown-item>
      <b-dropdown-item href="#">블레이져</b-dropdown-item>
      <b-dropdown-item href="#">숏패딩</b-dropdown-item>
      <b-dropdown-item href="#">조끼패딩</b-dropdown-item>
      <b-dropdown-item href="#">롱패딩</b-dropdown-item>
      <b-dropdown-item href="#">야구점퍼</b-dropdown-item>
      <b-dropdown-item href="#">항공점퍼</b-dropdown-item>
      <b-dropdown-item href="#">바람막이</b-dropdown-item>
      <b-dropdown-item href="#">야상</b-dropdown-item>
      <b-dropdown-item href="#">무스탕</b-dropdown-item>
      <b-dropdown-item href="#">코트</b-dropdown-item>
      <b-dropdown-item href="#">트랙탑</b-dropdown-item>
      <b-dropdown-item href="#">가죽자켓</b-dropdown-item>
      <b-dropdown-item href="#">청자켓</b-dropdown-item>
      <b-dropdown-item href="#">가디건</b-dropdown-item>
    </b-dropdown>
  <br/>
  <b-dropdown id="dropdown-dropright" dropright text="원피스" variant="outline-info" class="m-2" size="lg">
      <b-dropdown-item href="#">전체</b-dropdown-item>
    </b-dropdown>
  <br/>

</div>
</template>
<script>
export default {
  name: 'ClassificationComponent.vue'

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
