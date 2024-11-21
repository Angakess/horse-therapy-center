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
      <div v-for="(article, index) in noticias" :key="article.id" class="noticia">
        <h2 class="noticias-titulo">{{ article.title }}</h2>
        <h3 class="noticias-fecha">{{ formatDate(article.published_at) }}</h3>
        <p class="noticias-copete">{{ article.summary }}</p>

        <div v-if="isExpanded === index" class="noticias-contenido">
          <p>{{ article.content }}</p>
        </div>

        <!-- Botón para alternar la visibilidad del contenido completo -->
        <button @click="toggleContent(index)" class="read-more-btn">
          {{ isExpanded === index ? "Mostrar menos" : "Leer más" }}
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>
import { useNoticiaStore } from "../stores/noticia";
import { storeToRefs } from "pinia";
import { onMounted, ref } from "vue";

const isExpanded = ref(null);

const formatDate = (dateString) => {
  const options = { year: "numeric", month: "long", day: "numeric" };
  const date = new Date(dateString);
  return date.toLocaleDateString("es-ES", options);
};

const store = useNoticiaStore();
const { noticias, loading, error } = storeToRefs(store);

const fetchNoticias = async () => {
  await store.fetchNoticias();
};

// Función para alternar el contenido expandido de cada noticia
const toggleContent = (index) => {
  // Si ya está expandido, lo colapsamos. Si no, expandimos la nueva noticia.
  isExpanded.value = isExpanded.value === index ? null : index;
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

button {
    background: #0b6dff;
    border: 0;
    padding: 10px 20px;
    margin-top: 20px;
    color: white;
    border-radius: 20px;
    cursor: pointer;
  }


.noticias-contenido {
  margin-top: 10px;
  position: relative;
  z-index: 2;
}

.error {
  color: red;
  font-weight: bold;
}
</style>
