
    document.getElementById('images').addEventListener('change', function(e) {
      const preview = document.getElementById('imagePreview');
      preview.innerHTML = '';
      preview.style.display = 'flex';

      Array.from(e.target.files).forEach(file => {
        const reader = new FileReader();
        reader.onload = function(event) {
          const img = document.createElement('img');
          img.src = event.target.result;
          img.className = 'preview-img';
          img.style.display = 'block';
          preview.appendChild(img);
        };
        reader.readAsDataURL(file);
      });
    });

