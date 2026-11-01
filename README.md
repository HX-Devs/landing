# Helix — Landing

Primera base local del sitio, separada de `branding/`.

- `index.html`: estructura y textos.
- `styles.css`: diseño responsive.
- `assets/helix-motion.css`: animación CSS aprobada, ciclo de 4 segundos.
- `assets/helix-logo.svg` y `assets/helix-symbol.svg`: identidad vigente.

Abrir `index.html` en el navegador. No requiere instalación ni compilación. Los assets se copiaron desde branding para que esta carpeta sea autónoma. Si cambia la identidad, sincronizar las copias correspondientes.

Secciones iniciales: presentación, visión y principios. No se añadieron nombres de productos, clientes ni datos de contacto sin confirmar. Sitio publicado en https://helix.edfloreshz.dev/ mediante GitHub Pages.

La identidad usa astas principales de 28 unidades sobre una altura de 100, sin contornos añadidos. Los SVG, iconos y vista previa social están sincronizados con los maestros.

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

## Compartir enlaces y metadatos

La URL canónica se basa en el dominio de `CNAME`: https://helix.edfloreshz.dev/. El `<head>` contiene Open Graph, tarjeta grande de X/Twitter, descripción, URL canónica y datos estructurados de Organization/WebSite. Los bots pueden leer estas etiquetas sin ejecutar JavaScript.

- `assets/social-preview.png`: imagen pública para compartir (1200 × 630).
- `assets/icon-32.png`: favicon de respaldo.
- `assets/icon-180.png`: icono Apple Touch.
- `assets/icon-192.png` y `assets/icon-512.png`: iconos del manifiesto y logo para datos estructurados.
- `site.webmanifest`: nombre, descripción e iconos de la aplicación.
- `sitemap.xml`: URL canónica para buscadores.

Validar antes de publicar:

```sh
python3 scripts/validate_sharing.py
```

Si cambia el dominio, actualizar `CNAME`, las URLs absolutas en `index.html` y `sitemap.xml`. Las rutas de iconos del manifiesto son relativas. Publicar el HTML y los PNG juntos para evitar referencias rotas. Las redes sociales pueden conservar una vista previa anterior en caché; volver a solicitar el rastreo con su herramienta de depuración cuando esté disponible. Referencia de Open Graph: https://ogp.me/.
