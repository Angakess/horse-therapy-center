<template>
  <div>
    <h1>Contacto</h1>
    <form @submit.prevent="sendMessage">
      <div>
        <label for="nombre">Nombre completo:</label>
        <input type="text" id="nombre" v-model="formData.nya"/>
      </div>
      <div>
        <label for="email">Correo electrónico:</label>
        <input type="email" id="email" v-model="formData.email" />
      </div>
      <div>
        <label for="mensaje">Mensaje:</label>
        <textarea id="cuerpo" v-model="formData.cuerpo"></textarea>
      </div>

      <div id="recaptcha-container" class="g-recaptcha" style="margin: 10px 0;"></div>

      <button type="submit" :disabled="contactoStore.loading">Enviar</button>
      <p v-if="contactoStore.error" class="error">{{ contactoStore.error }}</p>
    </form>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import { useContactoStore } from "../stores/contacto";

export default {
  setup() {
    const contactoStore = useContactoStore();
    const formData = reactive({
      nya: "",
      email: "",
      cuerpo: "",
    });

    const renderCaptcha = () => {
      if (typeof grecaptcha !== "undefined") {
        if (document.getElementById("recaptcha-container").children.length === 0) {
          grecaptcha.render("recaptcha-container", {
            sitekey: "6LewOIUqAAAAAManxF2SdXH5Aqw-6gdARGvJ4zVv",
          });
        }
      } else {
        setTimeout(renderCaptcha, 500);
      }
    };

    const loadRecaptchaScript = () => {
      if (!document.getElementById("recaptcha-script")) {
        const script = document.createElement("script");
        script.id = "recaptcha-script";
        script.src = "https://www.google.com/recaptcha/api.js";
        script.async = true;
        script.defer = true;
        script.onload = renderCaptcha();
        document.head.appendChild(script);
      } else {
        renderCaptcha();
      }
    };

    onMounted(() => {
      loadRecaptchaScript();
    });

    const checkForm = () => {
      if (!formData.nya.length){
        contactoStore.error = "Nombre y apellido no ingresado.";
        return false;
      }
      if (!formData.email.length){
        contactoStore.error = "Correo no ingresado.";
        return false;
      }
      if (!formData.cuerpo.length){
        contactoStore.error = "Cuerpo del mensaje vacío.";
        return false;
      }
      return true;
    }

    const sendMessage = async () => {

      if (!checkForm()){
        return;
      }

      const captchaResponse = grecaptcha.getResponse();
      if (!captchaResponse || captchaResponse.length === 0) {
        contactoStore.error = "Captcha no resuelto.";
        return;
      }

      await contactoStore.sendMensaje({
        ...formData,
      });
      formData.nya = "";
      formData.email = "";
      formData.cuerpo = "";
      grecaptcha.reset();
    };

    return { contactoStore, formData, sendMessage};
  },
};
</script>



<style>
  input[type="text"],
  input[type="email"],
  textarea,
  select {
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
    cursor: pointer;
  }

  button:hover {
    background: #0066cc;
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

.g-recaptcha {
  display: block;
}

</style>
