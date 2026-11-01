# Helix — Landing

Primera base local del sitio, separada de `branding/`.

- `index.html`: estructura y textos.
- `styles.css`: diseño responsive.
- `assets/helix-motion.css`: animación CSS aprobada, ciclo de 4 segundos.
- `assets/helix-logo.svg` y `assets/helix-symbol.svg`: identidad vigente.

Abrir `index.html` en el navegador. No requiere instalación ni compilación. Los assets se copiaron desde branding para que esta carpeta sea autónoma. Si cambia la identidad, sincronizar las copias correspondientes.

Secciones iniciales: presentación, visión y principios. No se añadieron nombres de productos, clientes ni datos de contacto sin confirmar. Esta versión se mantiene local, sin publicación.

El logo del encabezado utiliza HX y HELIX con la misma altura visible. La animación mantiene una altura constante para ambos estados.

## Navbar y hero
El navbar comienza solo con el nombre HELIX. Al superar 64 px de scroll, se contrae al monograma HX; al volver a menos de 24 px, se expande al nombre. El pequeño margen entre umbrales evita parpadeos. `navigation.js` solo actualiza el estado del scroll; `navigation.css` realiza la compresión, el fundido y el rebote mediante una propiedad CSS interpolada. Los cambios de dirección retoman la posición actual. Con movimiento reducido, el cambio de estado es inmediato. Sin JavaScript se conserva el nombre completo.

El hero utiliza una imagen SVG estática del símbolo HX, sin animación.

## Fuentes de marca
- Logos maestros: `../branding/logos/horizontal/`.
- Símbolos maestros: `../branding/logos/symbols/`.
- Animación base: `../branding/animation/`.
- Guía: `../branding/guidelines/brand-guide.md`.

Las copias en `assets/` se conservan para que este landing sea autónomo.

## Apariencia automática
La página sigue `prefers-color-scheme` del dispositivo, incluso si cambia con la página abierta. El modo oscuro usa fondo verde carbón, texto marfil y acento arcilla claro. El navbar y su animación heredan el color de texto; el símbolo estático y el favicon usan la variante marfil en oscuro. El footer conserva su fondo negro y texto claro en ambos modos. No se requiere JavaScript ni almacenamiento para seleccionar el tema.
