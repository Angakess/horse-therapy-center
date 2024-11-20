import { defineStore } from "pinia";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
console.log("API Base URL:", API_BASE_URL)

export const useNoticiaStore = defineStore("noticia", {
    state: () => ({
      noticias: [],
      loading: false,
      error: null,
    }),

    actions:{
        async fetchNoticias(){
            try{
                this.loading = true
                this.error = null
    
                const response = await axios.get(`${API_BASE_URL}/api/contenido`)
                this.noticias = response.data
            }
            catch(error){
                this.error = "Error al obtener las noticias."
            }
            finally{
                this.loading = false
            }
        }
    }
})