import { defineStore } from "pinia";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const useContactoStore = defineStore("contacto", {
  state: () => ({
    contacto: [],
    loading: false,
    error: null,
  }),

  actions: {
    //Enviar un mensaje
    async sendMensaje(formData) {
      try {
        this.loading = true;
        this.error = null;

        const captchaResponse = grecaptcha.getResponse();

        if (captchaResponse.lenght === 0){
          this.error = "Captcha no resuelto";
          this.loading = false;
          return;
        }

        const response = await axios.post(`${API_BASE_URL}/api/contacto/messages`,formData);
        // Agregar el nuevo mensaje a la lista
        this.contacto.push(response.data);

      } catch (error) {
        this.error =
          error.response?.data?.message || "Ocurrió un error al enviar el mensaje.";
      } finally {
        this.loading = false;
      }
    },
  },
});
