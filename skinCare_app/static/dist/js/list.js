    const range = document.getElementById('priceRange');
    const value = document.getElementById('priceValue');
    value.textContent = '$' + range.value;
    range.addEventListener('input', () => {
      value.textContent = '$' + range.value;
    });