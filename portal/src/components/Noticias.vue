<template>
    <div class="noticias-list">
      <h1>Noticias</h1>
  
      <div v-if="loading">
        <p>Cargando noticias...</p>
      </div>
  
      <div v-if="!loading && !noticias.length">
        <p>No hay noticias disponibles en este momento.</p>
      </div>
  
      <div v-if="!loading && noticias.length">
        <div v-for="article in noticias">
          <h2 class="noticias-titulo">{{ article.title }}</h2>
          <h3 class="noticias-fecha">{{ formatDate(article.published_at) }}</h3>
          <p class="noticias-copete">{{ article.summary }}</p>
          <router-link :to="`/contenido/${article.content}`" class="read-more">Leer más...</router-link>
        </div>
      </div>

    </div>
  </template>
  
  <script setup>
    import { useNoticiaStore } from "../stores/noticia";
    import { storeToRefs } from "pinia";
    import { onMounted } from "vue";

    const formatDate = (dateString) => {
      console.log(dateString);
      const options = { year: "numeric", month: "long", day: "numeric" };
      const date = new Date(dateString);
      return date.toLocaleDateString("es-ES", options);
    };

    const store = useNoticiaStore();
    const  {noticias, loading, error} = storeToRefs(store)

    const fetchNoticias = async () => {
        await store.fetchNoticias();
    };

    onMounted(() => {
        if (!noticias.value.length) {
            fetchNoticias();
        }
    });

  </script>
  
  <style scoped>
  .news-list {
    padding: 20px;
  }
  
  .news-item {
    margin-bottom: 20px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 10px;
  }
  
  .news-date {
    font-size: 0.9em;
    color: #777;
  }
  
  .news-title {
    font-size: 1.5em;
    margin: 10px 0;
  }
  
  .news-summary {
    font-size: 1em;
    color: #444;
  }
  
  .read-more {
    display: inline-block;
    margin-top: 10px;
    font-weight: bold;
    color: #007bff;
  }
  
  .read-more:hover {
    text-decoration: underline;
  }
  
  .error {
    color: red;
    font-weight: bold;
  }
  </style>
  