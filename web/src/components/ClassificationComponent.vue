<template>
<div class="row">
    <div class="col-md-3">
        <div class="collaspe-panel">
            <div class="card-body">

            </div>

        </div>
    </div>

</div>
</template>

<script>
export default {
  name: 'ClassificationComponent.vue'

}
</script>

<style>
div {
    display: block;
}
.row {
    display: -ms-flexbox;
    display: flex;
    -ms-flex-wrap: wrap;
    flex-wrap: wrap;
    margin-right: -15px;
    margin-left: -15px;
}
col-md-3 {
    -ms-flex: 0 0 25%;
    flex: 0 0 25%;
    max-width: 25%;
}
.card-body {
    -ms-flex: 1 1 auto;
    flex: 1 1 auto;
    padding: 1.25rem;
}
</style>
