<template>
  <header>
    <img alt="Cedica logo" class="logo" src="@/assets/cedica.png" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="Bienvenidos a CEDICA" />

      <nav>
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/contacto">Contacto</RouterLink>
        <RouterLink to="/noticias">Noticias</RouterLink>

        <div class="social-media">
          <a href="https://www.instagram.com/cedica.equitacionparatodos/" target="_blank" rel="noopener">
            <img alt="Instagram" class="social-logo" src="@/assets/ig.png" width="24" height="24" />
          </a>
          <a href="https://www.facebook.com/cedica.equitacionparatodos/?locale=es_LA" target="_blank" rel="noopener">
            <img alt="Facebook" class="social-logo" src="@/assets/fc.png" width="24" height="24" />
          </a>
          <a href="https://x.com/CEDICA_" target="_blank" rel="noopener">
            <img alt="Facebook" class="social-logo" src="@/assets/tw.png" width="24" height="24" />
          </a>
        </div>
      </nav>
    </div>
  </header>

  <RouterView />
</template>


<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;

}

.logo {
  display: block;
  margin: 0 auto 2rem;

}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  display: center;
  margin-top: 2rem;
  

}

nav a.router-link-exact-active {
  color: var(--color-text);

}

nav a.router-link-exact-active:hover {
  background-color: transparent;

}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
  
}

nav a:first-of-type {
  border: 0;

}

/* Redes sociales */
.social-media {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem; 
}

.social-logo {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.social-logo:hover {
  opacity: 0.8; /* Efecto al pasar el cursor */
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
    
  }

  nav {
    text-align: center;
    margin-left: 1rem;
    font-size: 1rem;


    padding: 1rem 0;
    margin-top: 1rem;
  }

  .social-media {
    margin-top: 0.5rem;
  }
}

</style>
