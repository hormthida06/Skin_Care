    //
    //   // ==== CART FUNCTIONS ====
    //   function addToCartById(id) {
    //     const product = PRODUCTS.find(p => p.id === id);
    //     if (!product) return;
    //     const existing = cart.find(i => i.id === id);
    //     if (existing) existing.qty += 1;
    //     else cart.push({ id, qty: 1, checked: true });
    //     saveCart();
    //   }
    //
    //   function removeFromCart(id) {
    //     cart = cart.filter(i => i.id !== id);
    //     saveCart();
    //   }
    //
    //   function toggleItem(id) {
    //     const item = cart.find(i => i.id === id);
    //     if (item) item.checked = !item.checked;
    //     saveCart();
    //   }
    //
    //   function toggleSelectAll() {
    //     const checked = els.selectAll.checked;
    //     cart.forEach(i => i.checked = checked);
    //     saveCart();
    //   }
    //
    //   function saveCart() {
    //     localStorage.setItem("skincare_cart_v2", JSON.stringify(cart));
    //     renderCart();
    //     updateSummary();
    //   }
    //
    //   function renderCart() {
    //     const totalQty = cart.reduce((sum, i) => sum + i.qty, 0);
    //     els.cartCount.textContent = totalQty;
    //     els.cartTotalItems.textContent = totalQty;
    //
    //     if (cart.length === 0) {
    //         els.cartItems.innerHTML = '<p class="text-center text-muted py-5">Your cart is empty</p>';
    //         els.selectAll.checked = false;
    //         return;
    //     }
    //
    //     els.cartItems.innerHTML = cart.map(item => {
    //         const p = PRODUCTS.find(x => x.id === item.id);
    //         if (!p) return '';
    //
    //         const lineTotal = (p.price * item.qty).toFixed(2);
    //
    //         return `
    //         <div class="d-flex align-items-center gap-3 mb-3 p-3 border rounded bg-white">
    //             <input type="checkbox" class="form-check-input mt-0" ${item.checked ? 'checked' : ''}
    //                 onchange="toggleItem(${item.id})">
    //
    //             <img src="${p.image}" width="70" height="70" class="rounded object-fit-cover">
    //
    //             <div class="flex-grow-1">
    //             <h6 class="mb-1">${p.name}</h6>
    //             <small class="text-muted">$${p.price.toFixed(2)} each</small>
    //
    //             <div class="d-flex align-items-center gap-2 mt-2">
    //                 <button class="btn btn-sm btn-outline-secondary" onclick="updateQty(${item.id}, -1)">–</button>
    //                 <input type="number" value="${item.qty}" min="1" class="form-control form-control-sm text-center"
    //                     style="width:60px" onchange="updateQty(${item.id}, this.value - ${item.qty})">
    //                 <button class="btn btn-sm btn-outline-secondary" onclick="updateQty(${item.id}, 1)">+</button>
    //             </div>
    //             </div>
    //
    //             <div class="text-end">
    //             <strong class="d-block text-primary fs-5">$${lineTotal}</strong>
    //             <button class="btn btn-sm btn-danger mt-2" onclick="removeFromCart(${item.id})">
    //                 Remove
    //             </button>
    //             </div>
    //         </div>
    //             `;
    //     }).join('');
    //
    //     // Sync "Select All" checkbox
    //     const allChecked = cart.length > 0 && cart.every(i => i.checked);
    //     els.selectAll.checked = allChecked;
    //  }
    //
    //  function updateQty(id, change) {
    //     const item = cart.find(i => i.id === id);
    //     if (!item) return;
    //
    //     const newQty = item.qty + Number(change);
    //
    //     if (newQty < 1) {
    //         if (confirm("Remove this item from cart?")) {
    //         removeFromCart(id);
    //         }
    //         return;
    //     }
    //
    //     item.qty = newQty;
    //     saveCart(); // This calls renderCart() + updateSummary()
    //  }
    //
    //  function updateSummary() {
    //     const selected = cart.filter(i => i.checked);
    //     let subtotal = 0;
    //
    //     // Clear previous list
    //     els.checkoutList.innerHTML = selected.length === 0
    //         ? '<li class="text-muted small">No items selected</li>'
    //         : '';
    //
    //     // Build item list + calculate subtotal
    //     selected.forEach(item => {
    //         const p = PRODUCTS.find(x => x.id === item.id);
    //         if (!p) return;
    //         const lineTotal = p.price * item.qty;
    //         subtotal += lineTotal;
    //
    //         els.checkoutList.innerHTML += `
    //         <li class="d-flex justify-content-between py-1 small">
    //             <span>• ${p.name} × ${item.qty}</span>
    //             <strong>$${(lineTotal).toFixed(2)}</strong>
    //         </li>
    //         `;
    //     });
    //
    //     // Calculate final amounts
    //     const tax = subtotal * 0.10;
    //     const delivery = subtotal > 0 ? 2.50 : 0;
    //     const total = subtotal + tax + delivery;
    //
    //     // Update all values in BOTH cart offcanvas AND checkout modal
    //     document.querySelectorAll('#subtotal').forEach(el => el.textContent = '$' + subtotal.toFixed(2));
    //     document.querySelectorAll('#tax').forEach(el => el.textContent = '$' + tax.toFixed(2));
    //     document.querySelectorAll('#delivery').forEach(el => el.textContent = '$' + delivery.toFixed(2));
    //     document.querySelectorAll('#total').forEach(el => el.textContent = '$' + total.toFixed(2));
    //     document.querySelectorAll('#selected-count').forEach(el => el.textContent = selected.length);
    //     }
    //   // ==== CHECKOUT ====
    //  function openCheckout() {
    //     if (!currentUser) {
    //         alert('Please login first!');
    //         new bootstrap.Modal('#loginModal').show();
    //         return;
    //     }
    //     const selected = cart.filter(i => i.checked);
    //     if (selected.length === 0) {
    //         alert('Please select at least one item!');
    //         return;
    //     }
    //
    //     // These two lines are CRUCIAL
    //     document.getElementById('checkout-user').innerHTML = `
    //         <strong>${currentUser.name}</strong><br>
    //         <small>${currentUser.email}<br>${currentUser.phone || '—'}<br>${currentUser.address || '—'}</small>
    //     `;
    //
    //     updateSummary();  // ← This refreshes tax, total, items list
    //     new bootstrap.Modal('#checkoutModal').show();
    //     }
    //
    //  // ==== CHECKOUT PROCESS ====
    // function checkoutProcess() {
    //     const user = {
    //         name: "John Doe",
    //         email: "john@example.com",
    //         phone: "012345678",
    //         address: "Phnom Penh"
    //     };
    //
    //     // Get order items from UI
    //     const items = [];
    //     document.querySelectorAll("#checkout-list li").forEach(li => {
    //         items.push({
    //             name: li.dataset.name || li.innerText,
    //             qty: li.dataset.qty || 1
    //         });
    //     });
    //
    //     const total = document.getElementById("total").innerText;
    //
    //     const payload = {
    //         user: user,
    //         items: items,
    //         total: total
    //     };
    //
    //     fetch("http://127.0.0.1:8000/api/checkout/", {
    //         method: "POST",
    //         headers: {
    //             "Content-Type": "application/json"
    //         },
    //         body: JSON.stringify(payload)
    //     })
    //     .then(res => res.json())
    //     .then(data => {
    //         alert("Checkout successful!");
    //         console.log(data);
    //     })
    //     .catch(err => {
    //         console.error(err);
    //         alert("Checkout failed!");
    //     });
    // }
    //
    //
    // console.log("script.js loaded");
    //
    // function generateKHQR() {
    //     console.log("Generate KHQR clicked");
    //
    //     const totalAmount = parseFloat(
    //         document.getElementById("total").textContent.replace('$','')
    //     ) || 0;
    //
    //     fetch("http://127.0.0.1:5000/generate_khqr", {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json" },
    //         body: JSON.stringify({ amount: totalAmount })
    //     })
    //     .then(res => res.json())
    //     .then(data => {
    //
    //         console.log("QR DATA:", data.qrData);
    //
    //         const qrBox = document.getElementById("khqr-box");
    //         qrBox.innerHTML = "";
    //
    //         const canvas = document.createElement("canvas");
    //         qrBox.appendChild(canvas);
    //
    //         QRCode.toCanvas(canvas, data.qrData, function (error) {
    //             if (error) {
    //                 console.error(error);
    //                 qrBox.innerHTML = "<p>Failed to generate QR</p>";
    //             } else {
    //                 console.log(" KHQR generated!");
    //             }
    //         });
    //     })
    //     .catch(err => {
    //         console.error("FETCH ERROR:", err);
    //     });
    // }
    //
    //
    //   // ==== START ====
    //   init();
    //
