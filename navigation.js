(() => {
  const header = document.querySelector('.header');
  if (!header) return;
  let compact = false;
  let scheduled = false;
  function updateBrand() {
    scheduled = false;
    // Separate thresholds prevent flickering near the top of the page.
    const next = window.scrollY > (compact ? 24 : 64);
    if (next === compact) return;
    compact = next;
    header.classList.toggle('is-scrolled', compact);
  }
  window.addEventListener('scroll', () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(updateBrand);
  }, { passive: true });
  window.addEventListener('pageshow', updateBrand);
  updateBrand();
})();
