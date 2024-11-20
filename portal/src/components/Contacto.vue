<template>
    <div>
      <h1>Contacto</h1>
      <form @submit.prevent="sendMessage">
        <div>
          <label for="nombre">Nombre completo:</label>
          <input
            type="text"
            id="nombre"
            v-model="formData.nombre"
            required
          />
        </div>
        <div>
          <label for="email">Correo electrónico:</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            required
          />
        </div>
        <div>
          <label for="mensaje">Mensaje:</label>
          <textarea
            id="mensaje"
            v-model="formData.mensaje"
            required
          ></textarea>
        </div>
        <button type="submit" :disabled="contactoStore.loading">Enviar</button>
        <p v-if="contactoStore.error" class="error">{{ contactoStore.error }}</p>
        <p v-if="success" class="success">{{ success }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import { useContactoStore } from "@/stores/contacto";
  
  export default {
    data() {
      return {
        formData: {
          nombre: "",
          email: "",
          mensaje: "",
          captcha: "",
        },
        success: null, 
      };
    },
    setup() {
      const contactoStore = useContactoStore();
      return { contactoStore };
    },
    methods: {
      async sendMessage() {
        this.success = null;
        try {
          await this.contactoStore.sendMensaje(this.formData);
          this.success = "Mensaje enviado con éxito.";
          // Reiniciar formulario
          this.formData = {
            nombre: "",
            email: "",
            mensaje: "",
            captcha: "",
          };
        } catch (error) {
          // El error se gestiona desde el store
        }
      },
    },
  };
  </script>
<style>
    input[type=text], input[type=email], textarea, select {
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
        font-family: inherit;
        font-size: 16px;
    }

    textarea {
        resize: vertical;
    }

    button {
        background: #0b6dff;
        border: 0;
        padding: 10px 20px;
        margin-top: 20px;
        color: white;
        border-radius: 20px;
    }
    .submit {
        text-align: center;
    }

    .error {
        color: #ff0062;
        margin-top: 10px;
        font-size: 0.8em;
        font-weight: bold;
    }
</style>  