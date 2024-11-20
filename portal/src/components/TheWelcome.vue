<script setup>
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
</script>

<template>
  <WelcomeItem>
    <template #icon>
      <DocumentationIcon />
    </template>
    <template #heading>Clases</template>

    Ofrecemos clases de tacas y equinoterapia
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <ToolingIcon />
    </template>
    <template #heading>Modalidades de cursos</template>
    Contamos con cursos de modalidad tanto presencial como virtual.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <EcosystemIcon />
    </template>
    <template #heading>Desarrollo de tecnología adaptada</template>
    Contamos con el desarrollo de tecnologías adaptadas para la realización de las actividades.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <CommunityIcon />
    </template>
    <template #heading>¿Dónde encontrarnos?</template>
    Nos encontramos en la ciudad de La Plata, Buenos Aires, Argentina.
    <a href="https://maps.app.goo.gl/iHfDYugtvdLcn6as7" target="_blank" rel="noopener noreferrer">
      Ver en Google Maps
    </a>
  </WelcomeItem>
</template>
