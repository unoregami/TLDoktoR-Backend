document.addEventListener('DOMContentLoaded', () => {
  const output = document.getElementById('output');

  // Add fade-in for output content
  const observer = new MutationObserver(() => {
    output.classList.remove('fade-in');
    void output.offsetWidth; // reflow trick to restart animation
    output.classList.add('fade-in');
  });

  observer.observe(output, { childList: true });

  // Add shimmer loader effect
  const originalText = output.textContent;
  const shimmerHTML = `
    <div class="shimmer-container">
      <div class="shimmer-bar"></div>
    </div>
  `;

  const showLoading = (msg) => {
    output.innerHTML = `${msg}<br>${shimmerHTML}`;
  };

  // Listen for placeholder events (from popup.js)
  document.addEventListener('showLoading', (e) => showLoading(e.detail || 'Loading...'));

  // Example usage if you want to trigger:
  // document.dispatchEvent(new CustomEvent('showLoading', { detail: 'Summarizing...' }));
});
