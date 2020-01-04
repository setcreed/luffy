<template>
    <div class="home">
        <Header/>
        <Banner/>
    </div>
</template>

<script>
    import Header from '../components/Header'
    import Banner from "../components/Banner";

    export default {
        name: 'home',
        components: {
            Banner,
            Header
        }
    }
</script>
